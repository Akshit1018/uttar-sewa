"""
Google Cloud Firestore Database Service
Provides persistent cloud storage for video metadata and processing status
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from google.cloud import firestore
from google.oauth2 import service_account
import logging

logger = logging.getLogger(__name__)

class CloudDatabaseService:
    def __init__(self):
        self.db = None
        self.enabled = False
        self.initialize_firestore()
    
    def initialize_firestore(self):
        """Initialize Firestore connection"""
        try:
            # Check for service account key
            key_path = os.environ.get('GOOGLE_CLOUD_KEY_PATH', '/app/backend/google-cloud-key.json')
            
            if os.path.exists(key_path):
                credentials = service_account.Credentials.from_service_account_file(key_path)
                self.db = firestore.Client(credentials=credentials)
                self.enabled = True
                logger.info("Google Cloud Firestore initialized successfully")
            else:
                # Try using default credentials (for Cloud Run, etc.)
                try:
                    self.db = firestore.Client()
                    self.enabled = True
                    logger.info("Google Cloud Firestore initialized with default credentials")
                except Exception as e:
                    logger.warning(f"Could not initialize Firestore with default credentials: {e}")
                    self.enabled = False
        except Exception as e:
            logger.error(f"Failed to initialize Firestore: {e}")
            self.enabled = False
    
    async def sync_video_metadata(self, video_data: Dict[str, Any]) -> bool:
        """Sync video metadata to cloud database"""
        if not self.enabled:
            return False
        
        try:
            doc_ref = self.db.collection('videos').document(video_data['video_id'])
            
            # Prepare cloud document
            cloud_doc = {
                'video_id': video_data['video_id'],
                'title': video_data['title'],
                'description': video_data.get('description', ''),
                'duration': video_data.get('duration', ''),
                'upload_date': video_data.get('upload_date'),
                'view_count': video_data.get('view_count', 0),
                'transcript_processed': video_data.get('transcript_processed', False),
                'last_updated': firestore.SERVER_TIMESTAMP,
                'processing_status': video_data.get('processing_status', 'pending'),
                'qa_count': video_data.get('qa_count', 0),
                'language': video_data.get('language', 'hi'),
                'source': 'youtube_api'
            }
            
            # Use set with merge to update or create
            doc_ref.set(cloud_doc, merge=True)
            logger.debug(f"Synced video metadata for {video_data['video_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing video metadata: {e}")
            return False
    
    async def get_processed_video_ids(self) -> List[str]:
        """Get list of already processed video IDs from cloud"""
        if not self.enabled:
            return []
        
        try:
            # Query for processed videos
            processed_videos = self.db.collection('videos').where('transcript_processed', '==', True).stream()
            return [doc.id for doc in processed_videos]
        except Exception as e:
            logger.error(f"Error getting processed video IDs: {e}")
            return []
    
    async def get_all_video_ids(self) -> List[str]:
        """Get all video IDs from cloud database"""
        if not self.enabled:
            return []
        
        try:
            videos = self.db.collection('videos').stream()
            return [doc.id for doc in videos]
        except Exception as e:
            logger.error(f"Error getting all video IDs: {e}")
            return []
    
    async def get_videos_to_process(self) -> List[Dict[str, Any]]:
        """Get videos that need processing from cloud"""
        if not self.enabled:
            return []
        
        try:
            # Query for unprocessed videos
            unprocessed_query = self.db.collection('videos').where('transcript_processed', '==', False).limit(50)
            videos = []
            
            for doc in unprocessed_query.stream():
                video_data = doc.to_dict()
                video_data['id'] = doc.id
                videos.append(video_data)
            
            return videos
        except Exception as e:
            logger.error(f"Error getting videos to process: {e}")
            return []
    
    async def mark_video_processed(self, video_id: str, qa_count: int = 0) -> bool:
        """Mark video as processed in cloud database"""
        if not self.enabled:
            return False
        
        try:
            doc_ref = self.db.collection('videos').document(video_id)
            doc_ref.update({
                'transcript_processed': True,
                'processing_completed_at': firestore.SERVER_TIMESTAMP,
                'qa_count': qa_count,
                'last_updated': firestore.SERVER_TIMESTAMP
            })
            logger.debug(f"Marked video {video_id} as processed")
            return True
        except Exception as e:
            logger.error(f"Error marking video as processed: {e}")
            return False
    
    async def sync_qa_pairs(self, qa_pairs: List[Dict[str, Any]]) -> bool:
        """Sync Q&A pairs to cloud database"""
        if not self.enabled:
            return False
        
        try:
            batch = self.db.batch()
            
            for qa in qa_pairs:
                # Create unique ID for Q&A pair
                qa_id = f"{qa['video_id']}_{int(qa['start_time'])}"
                doc_ref = self.db.collection('question_answers').document(qa_id)
                
                cloud_qa = {
                    'video_id': qa['video_id'],
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'start_time': qa['start_time'],
                    'end_time': qa['end_time'],
                    'confidence_score': qa.get('confidence_score', 0.8),
                    'language': qa.get('language', 'hi'),
                    'tags': qa.get('tags', []),
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'source': 'youtube_processing'
                }
                
                batch.set(doc_ref, cloud_qa, merge=True)
            
            # Commit batch
            batch.commit()
            logger.debug(f"Synced {len(qa_pairs)} Q&A pairs to cloud")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing Q&A pairs: {e}")
            return False
    
    async def get_processing_statistics(self) -> Dict[str, Any]:
        """Get processing statistics from cloud database"""
        if not self.enabled:
            return {}
        
        try:
            # Get video counts
            total_videos = len(list(self.db.collection('videos').stream()))
            processed_videos = len(list(self.db.collection('videos').where('transcript_processed', '==', True).stream()))
            total_qa_pairs = len(list(self.db.collection('question_answers').stream()))
            
            # Get recent activity
            one_day_ago = datetime.utcnow().timestamp() - (24 * 60 * 60)
            
            return {
                'total_videos': total_videos,
                'processed_videos': processed_videos,
                'unprocessed_videos': total_videos - processed_videos,
                'total_qa_pairs': total_qa_pairs,
                'processing_percentage': round((processed_videos / total_videos * 100) if total_videos > 0 else 0, 2),
                'last_updated': datetime.utcnow().isoformat(),
                'cloud_sync_enabled': True
            }
        except Exception as e:
            logger.error(f"Error getting processing statistics: {e}")
            return {'cloud_sync_enabled': False, 'error': str(e)}
    
    async def backup_local_to_cloud(self, local_db) -> Dict[str, Any]:
        """Backup local MongoDB data to cloud Firestore"""
        if not self.enabled:
            return {'success': False, 'error': 'Cloud database not enabled'}
        
        try:
            backup_stats = {
                'videos_synced': 0,
                'qa_pairs_synced': 0,
                'errors': []
            }
            
            # Backup videos
            try:
                videos = await local_db.videos.find().to_list(None)
                for video in videos:
                    # Convert ObjectId to string and handle datetime
                    video_data = {
                        'video_id': video['video_id'],
                        'title': video['title'],
                        'description': video.get('description', ''),
                        'duration': video.get('duration', ''),
                        'upload_date': video.get('upload_date'),
                        'view_count': video.get('view_count', 0),
                        'transcript_processed': video.get('transcript_processed', False),
                        'created_at': video.get('created_at'),
                        'last_updated': firestore.SERVER_TIMESTAMP
                    }
                    
                    if await self.sync_video_metadata(video_data):
                        backup_stats['videos_synced'] += 1
                        
            except Exception as e:
                backup_stats['errors'].append(f"Video backup error: {str(e)}")
            
            # Backup Q&A pairs
            try:
                qa_pairs = await local_db.question_answers.find().to_list(None)
                qa_batch = []
                
                for qa in qa_pairs:
                    qa_data = {
                        'video_id': qa['video_id'],
                        'question': qa['question'],
                        'answer': qa['answer'],
                        'start_time': qa['start_time'],
                        'end_time': qa['end_time'],
                        'confidence_score': qa.get('confidence_score', 0.8),
                        'language': qa.get('language', 'hi'),
                        'tags': qa.get('tags', []),
                        'created_at': qa.get('created_at')
                    }
                    qa_batch.append(qa_data)
                    
                    # Process in batches of 100
                    if len(qa_batch) >= 100:
                        if await self.sync_qa_pairs(qa_batch):
                            backup_stats['qa_pairs_synced'] += len(qa_batch)
                        qa_batch = []
                
                # Process remaining items
                if qa_batch:
                    if await self.sync_qa_pairs(qa_batch):
                        backup_stats['qa_pairs_synced'] += len(qa_batch)
                        
            except Exception as e:
                backup_stats['errors'].append(f"Q&A backup error: {str(e)}")
            
            backup_stats['success'] = True
            backup_stats['timestamp'] = datetime.utcnow().isoformat()
            return backup_stats
            
        except Exception as e:
            logger.error(f"Error during backup: {e}")
            return {'success': False, 'error': str(e)}
    
    async def restore_from_cloud(self, local_db) -> Dict[str, Any]:
        """Restore data from cloud to local MongoDB"""
        if not self.enabled:
            return {'success': False, 'error': 'Cloud database not enabled'}
        
        try:
            restore_stats = {
                'videos_restored': 0,
                'qa_pairs_restored': 0,
                'errors': []
            }
            
            # Restore videos
            try:
                videos = self.db.collection('videos').stream()
                for doc in videos:
                    video_data = doc.to_dict()
                    # Convert Firestore timestamp back to datetime
                    if 'last_updated' in video_data:
                        del video_data['last_updated']  # Remove server timestamp
                    
                    # Insert or update in local DB
                    await local_db.videos.update_one(
                        {'video_id': video_data['video_id']},
                        {'$set': video_data},
                        upsert=True
                    )
                    restore_stats['videos_restored'] += 1
                    
            except Exception as e:
                restore_stats['errors'].append(f"Video restore error: {str(e)}")
            
            # Restore Q&A pairs
            try:
                qa_docs = self.db.collection('question_answers').stream()
                for doc in qa_docs:
                    qa_data = doc.to_dict()
                    # Remove server timestamps
                    if 'created_at' in qa_data and hasattr(qa_data['created_at'], 'timestamp'):
                        del qa_data['created_at']
                    
                    # Create unique identifier
                    qa_id = f"{qa_data['video_id']}_{int(qa_data['start_time'])}"
                    qa_data['id'] = qa_id
                    
                    # Insert or update in local DB
                    await local_db.question_answers.update_one(
                        {
                            'video_id': qa_data['video_id'],
                            'start_time': qa_data['start_time']
                        },
                        {'$set': qa_data},
                        upsert=True
                    )
                    restore_stats['qa_pairs_restored'] += 1
                    
            except Exception as e:
                restore_stats['errors'].append(f"Q&A restore error: {str(e)}")
            
            restore_stats['success'] = True
            restore_stats['timestamp'] = datetime.utcnow().isoformat()
            return restore_stats
            
        except Exception as e:
            logger.error(f"Error during restore: {e}")
            return {'success': False, 'error': str(e)}

# Global instance
cloud_db = CloudDatabaseService()