import React, { useState, useEffect } from 'react';
import { BarChart3, Users, Database, TrendingUp, RefreshCw, Download, Trash2, Settings, Eye, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { useToast } from '../hooks/use-toast';
import { analyticsService } from '../services/analyticsService';
import PageShell from './Layout/PageShell';

import { API } from '../lib/backend';
import { controlHeaders } from '../lib/control';

const AdminDashboard = ({ language }) => {
  const [stats, setStats] = useState(null);
  const [systemStatus, setSystemStatus] = useState(null);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load system stats
      const [statsResponse, systemResponse] = await Promise.all([
        fetch(`${API}/stats`),
        fetch(`${API}/system/status`)
      ]);

      const statsData = await statsResponse.json();
      const systemData = await systemResponse.json();
      
      setStats(statsData);
      setSystemStatus(systemData);
      
      // Load analytics data
      const analytics = analyticsService.exportData();
      setAnalyticsData(analytics);
      
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast({
        title: language === 'hi' ? 'डेटा लोड करने में त्रुटि' : 'Error Loading Data',
        description: error.message,
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleClearProcessingStatus = async () => {
    try {
      const response = await fetch(`${API}/process/clear`, { method: 'POST', headers: controlHeaders() });
      if (response.ok) {
        toast({
          title: language === 'hi' ? 'प्रोसेसिंग स्थिति साफ की गई' : 'Processing Status Cleared',
          description: language === 'hi' ? 'सभी प्रोसेसिंग स्थिति रीसेट हो गई' : 'All processing status has been reset'
        });
        loadDashboardData();
      }
    } catch (error) {
      console.error('Error clearing processing status:', error);
    }
  };

  const handleExportAnalytics = () => {
    const data = analyticsService.exportData();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `spiritual-qa-analytics-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    toast({
      title: language === 'hi' ? 'एनालिटिक्स एक्सपोर्ट हुआ' : 'Analytics Exported',
      description: language === 'hi' ? 'डेटा सफलतापूर्वक डाउनलोड हुआ' : 'Data downloaded successfully'
    });
  };

  const handleClearAnalytics = () => {
    analyticsService.clearData();
    setAnalyticsData(analyticsService.exportData());
    toast({
      title: language === 'hi' ? 'एनालिटिक्स साफ किया गया' : 'Analytics Cleared',
      description: language === 'hi' ? 'सभी एनालिटिक्स डेटा हटा दिया गया' : 'All analytics data has been cleared'
    });
  };

  if (loading) {
    return (
      <PageShell wide>
        <div className="flex items-center justify-center py-16">
          <div className="text-center">
            <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4" />
            <p>{language === 'hi' ? 'डैशबोर्ड लोड हो रहा है...' : 'Loading Dashboard...'}</p>
          </div>
        </div>
      </PageShell>
    );
  }

  return (
    <PageShell wide>
      <div>
        {/* Header */}
        <div className="mb-6 sm:mb-8">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="min-w-0">
              <h1 className="text-xl sm:text-2xl font-bold text-white mb-2 flex items-center gap-3">
                <BarChart3 className="w-6 h-6 shrink-0" />
                {language === 'hi' ? 'एडमिन डैशबोर्ड' : 'Admin Dashboard'}
              </h1>
              <p className="text-gray-400 text-sm">
                {language === 'hi' ? 'सिस्टम स्थिति और एनालिटिक्स' : 'System Status and Analytics'}
              </p>
            </div>
            <Button
              onClick={loadDashboardData}
              variant="outline"
              className="border-white/20 text-gray-300 hover:bg-white/10 w-full sm:w-auto"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              {language === 'hi' ? 'रिफ्रेश' : 'Refresh'}
            </Button>
          </div>
        </div>

        {/* System Overview Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 sm:gap-6 mb-8">
          {stats && [
            {
              title: language === 'hi' ? 'कुल वीडियो' : 'Total Videos',
              value: stats.total_videos,
              icon: Database,
              color: 'from-blue-500/20 to-blue-500/5'
            },
            {
              title: language === 'hi' ? 'प्रोसेस्ड वीडियो' : 'Processed Videos',
              value: stats.processed_videos,
              icon: TrendingUp,
              color: 'from-green-500/20 to-green-500/5'
            },
            {
              title: language === 'hi' ? 'कुल Q&A' : 'Total Q&As',
              value: stats.total_qa_pairs,
              icon: Users,
              color: 'from-purple-500/20 to-purple-500/5'
            },
            {
              title: language === 'hi' ? 'प्रोसेसिंग प्रगति' : 'Processing Progress',
              value: stats.total_videos > 0 ? Math.round((stats.processed_videos / stats.total_videos) * 100) + '%' : '0%',
              icon: BarChart3,
              color: 'from-orange-500/20 to-orange-500/5'
            }
          ].map((stat, index) => {
            const IconComponent = stat.icon;
            return (
              <Card key={index} className="glass-card rounded-2xl">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-gray-400 text-sm font-medium">{stat.title}</p>
                      <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
                    </div>
                    <div className={`w-12 h-12 bg-gradient-to-r ${stat.color} rounded-xl flex items-center justify-center`}>
                      <IconComponent className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* System Status */}
        {systemStatus && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-8">
            <Card className="glass-card rounded-2xl">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Database className="w-5 h-5" />
                  {language === 'hi' ? 'डेटाबेस स्थिति' : 'Database Status'}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">{language === 'hi' ? 'प्रोसेसिंग प्रगति' : 'Processing Progress'}</span>
                    <span className="text-white">
                      {systemStatus.database.processed_videos}/{systemStatus.database.total_videos}
                    </span>
                  </div>
                  <Progress
                    value={
                      systemStatus.database.total_videos > 0
                        ? (systemStatus.database.processed_videos / systemStatus.database.total_videos) * 100
                        : 0
                    }
                    className="h-2"
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4 pt-4">
                  <div className="text-center">
                    <p className="text-lg font-bold text-white">{systemStatus.database.total_qa_pairs}</p>
                    <p className="text-xs text-gray-400">{language === 'hi' ? 'Q&A जोड़े' : 'Q&A Pairs'}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-bold text-white">{systemStatus.database.unprocessed_videos}</p>
                    <p className="text-xs text-gray-400">{language === 'hi' ? 'बाकी वीडियो' : 'Remaining Videos'}</p>
                  </div>
                </div>

                <div className="flex items-center gap-2 pt-2">
                  <div className={`w-2 h-2 rounded-full ${systemStatus.database.real_data_only ? 'bg-green-400' : 'bg-yellow-400'}`}></div>
                  <span className="text-sm text-gray-400">
                    {systemStatus.database.real_data_only 
                      ? (language === 'hi' ? 'केवल वास्तविक डेटा' : 'Real Data Only')
                      : (language === 'hi' ? 'नमूना डेटा शामिल' : 'Sample Data Included')
                    }
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card rounded-2xl">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Settings className="w-5 h-5" />
                  {language === 'hi' ? 'प्रोसेसिंग स्थिति' : 'Processing Status'}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">{language === 'hi' ? 'सक्रिय प्रोसेसिंग' : 'Active Processing'}</span>
                  <Badge className={`${systemStatus.processing.is_active ? 'bg-green-500/20 text-green-400' : 'bg-gray-500/20 text-gray-400'}`}>
                    {systemStatus.processing.is_active 
                      ? (language === 'hi' ? 'चालू' : 'Active')
                      : (language === 'hi' ? 'बंद' : 'Inactive')
                    }
                  </Badge>
                </div>

                {systemStatus.processing.current_status && (
                  <div>
                    <p className="text-sm text-gray-400 mb-1">{language === 'hi' ? 'वर्तमान स्थिति' : 'Current Status'}</p>
                    <p className="text-white font-medium">{systemStatus.processing.current_status}</p>
                    {systemStatus.processing.current_progress && (
                      <p className="text-sm text-gray-400 mt-1">
                        {language === 'hi' ? 'प्रगति:' : 'Progress:'} {systemStatus.processing.current_progress}
                      </p>
                    )}
                  </div>
                )}

                <div className="space-y-2">
                  <p className="text-sm text-gray-400">{language === 'hi' ? 'API कॉल्स आवश्यक' : 'API Calls Needed'}</p>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="bg-white/5 rounded-lg p-2 text-center">
                      <p className="text-white font-medium">{systemStatus.api_optimization.youtube_api_calls_needed}</p>
                      <p className="text-gray-400">YouTube</p>
                    </div>
                    <div className="bg-white/5 rounded-lg p-2 text-center">
                      <p className="text-white font-medium">{systemStatus.api_optimization.gemini_api_calls_needed}</p>
                      <p className="text-gray-400">Gemini</p>
                    </div>
                  </div>
                </div>

                <Button
                  onClick={handleClearProcessingStatus}
                  variant="outline"
                  className="w-full border-red-500/50 text-red-400 hover:bg-red-500/10"
                >
                  <Trash2 className="w-4 h-4 mr-2" />
                  {language === 'hi' ? 'प्रोसेसिंग स्थिति साफ करें' : 'Clear Processing Status'}
                </Button>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Analytics Section */}
        {analyticsData && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-8">
            <Card className="glass-card rounded-2xl">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  {language === 'hi' ? 'उपयोग एनालिटिक्स' : 'Usage Analytics'}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-white">{analyticsData.user_insights.total_sessions}</p>
                    <p className="text-sm text-gray-400">{language === 'hi' ? 'सत्र' : 'Sessions'}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-white">{analyticsData.user_insights.total_searches}</p>
                    <p className="text-sm text-gray-400">{language === 'hi' ? 'खोजें' : 'Searches'}</p>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">{language === 'hi' ? 'औसत खोज समय' : 'Avg Search Time'}</span>
                    <span className="text-white">{Math.round(analyticsData.user_insights.avg_search_time)}ms</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">{language === 'hi' ? 'भाषा बदलाव' : 'Language Switches'}</span>
                    <span className="text-white">{analyticsData.user_insights.language_switches}</span>
                  </div>
                </div>

                <div className="pt-2">
                  <p className="text-sm text-gray-400 mb-2">{language === 'hi' ? 'उपयोग की गई भाषाएं' : 'Languages Used'}</p>
                  <div className="flex flex-wrap gap-1">
                    {analyticsData.user_insights.languages_used.map((lang, index) => (
                      <Badge key={index} variant="secondary" className="bg-white/20 text-white text-xs">
                        {lang}
                      </Badge>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card rounded-2xl">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Eye className="w-5 h-5" />
                  {language === 'hi' ? 'सत्र जानकारी' : 'Session Info'}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <p className="text-lg font-bold text-white">{analyticsData.session_stats.total_events}</p>
                    <p className="text-sm text-gray-400">{language === 'hi' ? 'इवेंट्स' : 'Events'}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-bold text-white">{analyticsData.session_stats.searches_performed}</p>
                    <p className="text-sm text-gray-400">{language === 'hi' ? 'खोजें' : 'Searches'}</p>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">{language === 'hi' ? 'सत्र अवधि' : 'Session Duration'}</span>
                    <span className="text-white">
                      {Math.round(analyticsData.session_stats.session_duration / 1000 / 60)}m
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">{language === 'hi' ? 'वीडियो क्लिक्स' : 'Video Clicks'}</span>
                    <span className="text-white">{analyticsData.session_stats.videos_clicked}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">{language === 'hi' ? 'अद्वितीय प्रश्न' : 'Unique Queries'}</span>
                    <span className="text-white">{analyticsData.session_stats.unique_queries}</span>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row gap-2 pt-4">
                  <Button
                    onClick={handleExportAnalytics}
                    variant="outline"
                    className="flex-1 border-white/20 text-gray-300 hover:bg-white/10"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    {language === 'hi' ? 'एक्सपोर्ट' : 'Export'}
                  </Button>
                  <Button
                    onClick={handleClearAnalytics}
                    variant="outline"
                    className="flex-1 border-red-500/50 text-red-400 hover:bg-red-500/10"
                  >
                    <Trash2 className="w-4 h-4 mr-2" />
                    {language === 'hi' ? 'साफ करें' : 'Clear'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* System Health Alerts */}
        <Card className="glass-card rounded-2xl">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-yellow-400" />
              {language === 'hi' ? 'सिस्टम अलर्ट' : 'System Alerts'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {systemStatus && systemStatus.database.unprocessed_videos > 0 && (
                <div className="flex items-center gap-3 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                  <AlertTriangle className="w-5 h-5 text-yellow-400 flex-shrink-0" />
                  <div>
                    <p className="text-white font-medium text-sm">
                      {language === 'hi' ? 'कैप्शन रहित कतार' : 'Missing-caption queue'}
                    </p>
                    <p className="text-gray-400 text-xs">
                      {language === 'hi'
                        ? `${systemStatus.database.unprocessed_videos} वीडियो अभी उद्धृत नहीं हो सकते। कैप्शन या बाद में Whisper से ट्रांसक्रिप्ट चाहिए।`
                        : `${systemStatus.database.unprocessed_videos} videos cannot be cited yet. They need captions or later Whisper transcripts.`}
                    </p>
                  </div>
                </div>
              )}

              {stats && stats.processed_videos === 0 && (
                <div className="flex items-center gap-3 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                  <AlertTriangle className="w-5 h-5 text-yellow-400 flex-shrink-0" />
                  <div>
                    <p className="text-white font-medium text-sm">
                      {language === 'hi' ? 'वीडियो प्रोसेसिंग आवश्यक' : 'Video Processing Required'}
                    </p>
                    <p className="text-gray-400 text-xs">
                      {language === 'hi' 
                        ? 'कोई वीडियो अभी तक प्रोसेस नहीं हुआ है। खोज सुविधा को सक्रिय करने के लिए प्रोसेसिंग शुरू करें।'
                        : 'No videos have been processed yet. Start processing to enable search functionality.'
                      }
                    </p>
                  </div>
                </div>
              )}

              {systemStatus && systemStatus.processing.is_active && (
                <div className="flex items-center gap-3 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                  <RefreshCw className="w-5 h-5 text-blue-400 flex-shrink-0 animate-spin" />
                  <div>
                    <p className="text-white font-medium text-sm">
                      {language === 'hi' ? 'प्रोसेसिंग चल रही है' : 'Processing in Progress'}
                    </p>
                    <p className="text-gray-400 text-xs">
                      {systemStatus.processing.current_progress}
                    </p>
                  </div>
                </div>
              )}

              {!systemStatus?.database.real_data_only && (
                <div className="flex items-center gap-3 p-3 bg-orange-500/10 border border-orange-500/20 rounded-lg">
                  <Database className="w-5 h-5 text-orange-400 flex-shrink-0" />
                  <div>
                    <p className="text-white font-medium text-sm">
                      {language === 'hi' ? 'नमूना डेटा मौजूद' : 'Sample Data Present'}
                    </p>
                    <p className="text-gray-400 text-xs">
                      {language === 'hi' 
                        ? 'डेटाबेस में अभी भी कुछ नमूना डेटा है। केवल वास्तविक डेटा के लिए डेटाबेस साफ करें।'
                        : 'Database still contains some sample data. Clear database for real data only.'
                      }
                    </p>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </PageShell>
  );
};

export default AdminDashboard;