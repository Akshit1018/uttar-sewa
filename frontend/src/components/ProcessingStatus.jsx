import React, { useState, useEffect } from 'react';
import { Loader2, CheckCircle, AlertCircle, Play, Database, RefreshCw, Plus, Link, Globe } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { useToast } from '../hooks/use-toast';
import { t } from '../utils/translations';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ProcessingStatus = ({ language }) => {
  const [processingStatus, setProcessingStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statusId, setStatusId] = useState(null);
  const [customChannelUrl, setCustomChannelUrl] = useState('');
  const [showCustomChannel, setShowCustomChannel] = useState(false);
  const [systemStatus, setSystemStatus] = useState(null);
  const { toast } = useToast();

  useEffect(() => {
    loadSystemStatus();
    const savedStatusId = localStorage.getItem('processingStatusId');
    if (savedStatusId) {
      setStatusId(savedStatusId);
      checkProcessingStatus(savedStatusId);
    }
  }, []);

  useEffect(() => {
    let interval;
    if (statusId && processingStatus?.status === 'processing') {
      interval = setInterval(() => {
        checkProcessingStatus(statusId);
      }, 5000);
    }
    return () => clearInterval(interval);
  }, [statusId, processingStatus?.status]);

  const loadSystemStatus = async () => {
    try {
      const response = await fetch(`${API}/system/status`);
      if (response.ok) {
        const data = await response.json();
        setSystemStatus(data);
      }
    } catch (error) {
      console.error('Error loading system status:', error);
    }
  };

  const startProcessing = async (channelUrl = null) => {
    setLoading(true);
    try {
      const requestBody = channelUrl 
        ? { channel_url: channelUrl }
        : {};

      const response = await fetch(`${API}/process/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error('Failed to start processing');
      }

      const data = await response.json();
      setStatusId(data.status_id);
      localStorage.setItem('processingStatusId', data.status_id);
      
      toast({
        title: t('processingStarted', language),
        description: channelUrl 
          ? (language === 'hi' ? 'नए चैनल की प्रोसेसिंग शुरू हो गई' : 'Custom channel processing started')
          : t('processingStartedDesc', language),
      });

      setShowCustomChannel(false);
      setCustomChannelUrl('');
      checkProcessingStatus(data.status_id);
    } catch (error) {
      console.error('Error starting processing:', error);
      toast({
        title: t('processingError', language),
        description: error.message || t('processingErrorDesc', language),
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const clearProcessingStatus = async () => {
    try {
      const response = await fetch(`${API}/process/clear`, {
        method: 'POST'
      });
      
      if (response.ok) {
        localStorage.removeItem('processingStatusId');
        setStatusId(null);
        setProcessingStatus(null);
        
        toast({
          title: language === 'hi' ? 'स्थिति साफ़ की गई' : 'Status Cleared',
          description: language === 'hi' ? 'आप नई प्रोसेसिंग शुरू कर सकते हैं' : 'You can start fresh processing',
        });
      }
    } catch (error) {
      console.error('Error clearing status:', error);
      toast({
        title: language === 'hi' ? 'त्रुटि' : 'Error',
        description: language === 'hi' ? 'स्थिति साफ़ करने में समस्या' : 'Problem clearing status',
        variant: "destructive"
      });
    }
  };

  const checkProcessingStatus = async (id) => {
    try {
      const response = await fetch(`${API}/process/status/${id}`);
      if (response.ok) {
        const data = await response.json();
        setProcessingStatus(data);

        if (data.status === 'completed') {
          localStorage.removeItem('processingStatusId');
          toast({
            title: t('processingComplete', language),
            description: t('processingCompleteDesc', language),
          });
        } else if (data.status === 'failed') {
          localStorage.removeItem('processingStatusId');
          toast({
            title: language === 'hi' ? 'प्रोसेसिंग में त्रुटि' : 'Processing Error',
            description: data.error_message || (language === 'hi' ? 'कुछ गलत हुआ है' : 'Something went wrong'),
            variant: "destructive"
          });
        }
      }
    } catch (error) {
      console.error('Error checking status:', error);
    }
  };

  const validateYouTubeUrl = (url) => {
    const youtubeRegex = /^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
    return youtubeRegex.test(url);
  };

  const handleCustomChannelSubmit = () => {
    if (!customChannelUrl.trim()) {
      toast({
        title: language === 'hi' ? 'URL दर्ज करें' : 'Enter URL',
        description: language === 'hi' ? 'कृपया YouTube चैनल का URL दर्ज करें' : 'Please enter a YouTube channel URL',
        variant: "destructive"
      });
      return;
    }

    if (!validateYouTubeUrl(customChannelUrl)) {
      toast({
        title: language === 'hi' ? 'गलत URL' : 'Invalid URL',
        description: language === 'hi' ? 'कृपया सही YouTube चैनल URL दर्ज करें' : 'Please enter a valid YouTube channel URL',
        variant: "destructive"
      });
      return;
    }

    startProcessing(customChannelUrl);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending':
        return 'from-yellow-500/20 to-yellow-500/10';
      case 'processing':
        return 'from-blue-500/20 to-blue-500/10';
      case 'completed':
        return 'from-green-500/20 to-green-500/10';
      case 'failed':
        return 'from-red-500/20 to-red-500/10';
      default:
        return 'from-white/20 to-white/10';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'processing':
        return <Loader2 className="w-6 h-6 animate-spin" />;
      case 'completed':
        return <CheckCircle className="w-6 h-6 text-green-400" />;
      case 'failed':
        return <AlertCircle className="w-6 h-6 text-red-400" />;
      default:
        return <Database className="w-6 h-6" />;
    }
  };

  const getStatusText = (status) => {
    return t(status, language);
  };

  const isProcessingActive = processingStatus?.status === 'processing' || processingStatus?.status === 'pending';
  const canStartProcessing = !isProcessingActive && !loading;

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="px-4 py-8 sm:px-6">
        <Card className="glass-card rounded-2xl shadow-2xl overflow-hidden">
          <CardHeader className="bg-white/5 border-b border-white/10">
            <CardTitle className="text-white flex items-center gap-3 text-lg">
              <div className="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center">
                <Database className="w-5 h-5 text-white" />
              </div>
              {t('processingTitle', language)}
            </CardTitle>
          </CardHeader>
          
          <CardContent className="p-6 space-y-6">
            {/* System Status Overview */}
            {systemStatus && (
              <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                <h3 className="text-white font-medium mb-3 flex items-center gap-2">
                  <Globe className="w-4 h-4" />
                  {language === 'hi' ? 'सिस्टम स्थिति' : 'System Status'}
                </h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-400">{language === 'hi' ? 'कुल वीडियो:' : 'Total Videos:'}</span>
                    <span className="text-white ml-2">{systemStatus.database.total_videos}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">{language === 'hi' ? 'प्रोसेस्ड:' : 'Processed:'}</span>
                    <span className="text-white ml-2">{systemStatus.database.processed_videos}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">{language === 'hi' ? 'Q&A जोड़े:' : 'Q&A Pairs:'}</span>
                    <span className="text-white ml-2">{systemStatus.database.total_qa_pairs}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">{language === 'hi' ? 'प्रगति:' : 'Progress:'}</span>
                    <span className="text-white ml-2">{systemStatus.database.processing_progress}</span>
                  </div>
                </div>
              </div>
            )}

            {!statusId && !processingStatus ? (
              <div className="text-center py-8">
                <div className="w-20 h-20 bg-white/5 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Play className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">
                  {t('startProcessing', language)}
                </h3>
                <p className="text-gray-400 mb-6 text-sm max-w-sm mx-auto leading-relaxed">
                  {t('startProcessingDesc', language)}
                </p>

                <div className="space-y-4">
                  {/* Default Processing Button */}
                  <Button
                    onClick={() => startProcessing()}
                    disabled={loading}
                    className="bg-white text-black hover:bg-gray-100 font-semibold px-8 py-3 rounded-xl transition-all duration-300 text-sm w-full sm:w-auto"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        {language === 'hi' ? 'शुरू हो रहा है...' : 'Starting...'}
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4 mr-2" />
                        {t('startProcessing', language)}
                      </>
                    )}
                  </Button>

                  {/* Custom Channel Processing */}
                  <div className="pt-4 border-t border-white/10">
                    <Button
                      onClick={() => setShowCustomChannel(!showCustomChannel)}
                      variant="outline"
                      className="border-white/20 text-gray-300 hover:bg-white/10 w-full sm:w-auto"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      {language === 'hi' ? 'कस्टम चैनल प्रोसेस करें' : 'Process Custom Channel'}
                    </Button>

                    {showCustomChannel && (
                      <div className="mt-4 space-y-3 glass-card rounded-xl p-4">
                        <h4 className="text-white font-medium text-sm">
                          {language === 'hi' ? 'YouTube चैनल URL दर्ज करें' : 'Enter YouTube Channel URL'}
                        </h4>
                        <div className="flex gap-2">
                          <Input
                            type="url"
                            placeholder="https://www.youtube.com/@channelname"
                            value={customChannelUrl}
                            onChange={(e) => setCustomChannelUrl(e.target.value)}
                            className="bg-white/5 border-white/20 text-white placeholder-gray-400 flex-1"
                          />
                          <Button
                            onClick={handleCustomChannelSubmit}
                            disabled={loading}
                            className="bg-white text-black hover:bg-gray-100"
                          >
                            {loading ? (
                              <Loader2 className="w-4 h-4 animate-spin" />
                            ) : (
                              <Link className="w-4 h-4" />
                            )}
                          </Button>
                        </div>
                        <p className="text-xs text-gray-400">
                          {language === 'hi' 
                            ? 'आप किसी भी YouTube चैनल को प्रोसेस कर सकते हैं। चैनल का पूरा URL दर्ज करें।'
                            : 'You can process any YouTube channel. Enter the full channel URL.'
                          }
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Status Header */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 bg-gradient-to-r ${getStatusColor(processingStatus?.status)} rounded-xl flex items-center justify-center`}>
                      {getStatusIcon(processingStatus?.status)}
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-white">
                        {getStatusText(processingStatus?.status)}
                      </h3>
                      <p className="text-gray-400 text-sm">
                        {processingStatus?.status === 'processing' 
                          ? (language === 'hi' ? 'वीडियो प्रोसेस हो रहे हैं...' : 'Processing videos...')
                          : (language === 'hi' ? 'स्थिति अपडेट' : 'Status update')
                        }
                      </p>
                    </div>
                  </div>
                  <Badge className={`${
                    processingStatus?.status === 'processing' ? 'bg-blue-500/20 text-blue-400' :
                    processingStatus?.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                    processingStatus?.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                    'bg-white/10 text-white'
                  } px-3 py-1 rounded-full text-xs`}>
                    {processingStatus?.status?.toUpperCase()}
                  </Badge>
                </div>

                {/* Progress Section */}
                {processingStatus && (
                  <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="flex justify-between text-sm font-medium text-white mb-3">
                      <span>{t('progress', language)}</span>
                      <span className="text-white">
                        {processingStatus.processed_videos || 0} / {processingStatus.total_videos || 0}
                      </span>
                    </div>
                    <Progress
                      value={
                        processingStatus.total_videos > 0
                          ? (processingStatus.processed_videos / processingStatus.total_videos) * 100
                          : 0
                      }
                      className="h-3 bg-white/10 rounded-full"
                    />
                    <div className="text-right text-xs text-gray-400 mt-2">
                      {processingStatus.total_videos > 0 
                        ? Math.round((processingStatus.processed_videos / processingStatus.total_videos) * 100)
                        : 0
                      }% {language === 'hi' ? 'पूर्ण' : 'Complete'}
                    </div>
                  </div>
                )}

                {/* Current Video */}
                {processingStatus?.current_video_title && (
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <div className="text-white font-medium mb-2 flex items-center gap-2 text-sm">
                      <Play className="w-4 h-4" />
                      {t('currentVideo', language)}
                    </div>
                    <div className="text-white text-sm leading-relaxed">
                      {processingStatus.current_video_title}
                    </div>
                  </div>
                )}

                {/* Error Message */}
                {processingStatus?.error_message && (
                  <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4">
                    <div className="text-white font-medium flex items-center gap-2 mb-2 text-sm">
                      <AlertCircle className="w-4 h-4 text-red-400" />
                      {language === 'hi' ? 'त्रुटि विवरण:' : 'Error Details:'}
                    </div>
                    <div className="text-gray-300 text-sm">
                      {processingStatus.error_message}
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex flex-col sm:flex-row gap-3">
                  <Button
                    onClick={() => checkProcessingStatus(statusId)}
                    variant="outline"
                    className="border-white/20 text-gray-300 hover:bg-white/10 rounded-xl px-4 py-3 flex-1"
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    {t('refreshStatus', language)}
                  </Button>
                  
                  <Button
                    onClick={clearProcessingStatus}
                    variant="outline"
                    className="border-white/20 text-gray-300 hover:bg-white/10 rounded-xl px-4 py-3 flex-1"
                  >
                    {language === 'hi' ? 'स्थिति साफ़ करें' : 'Clear Status'}
                  </Button>
                  
                  {processingStatus?.status === 'completed' && (
                    <Button
                      onClick={() => window.location.reload()}
                      className="bg-white text-black hover:bg-gray-100 rounded-xl px-4 py-3 flex-1"
                    >
                      <CheckCircle className="w-4 h-4 mr-2" />
                      {t('startSearch', language)}
                    </Button>
                  )}
                </div>

                {/* Start New Processing (if current is complete/failed) */}
                {canStartProcessing && processingStatus?.status !== 'processing' && (
                  <div className="pt-4 border-t border-white/10">
                    <Button
                      onClick={() => startProcessing()}
                      className="bg-white text-black hover:bg-gray-100 font-semibold px-6 py-3 rounded-xl w-full sm:w-auto"
                    >
                      <Play className="w-4 h-4 mr-2" />
                      {language === 'hi' ? 'नई प्रोसेसिंग शुरू करें' : 'Start New Processing'}
                    </Button>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProcessingStatus;