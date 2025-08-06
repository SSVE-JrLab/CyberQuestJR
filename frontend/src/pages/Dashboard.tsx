import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { progressAPI } from '../services/api';
import { Progress } from '../types';
import { 
  Brain, 
  BookOpen, 
  Trophy, 
  Target, 
  Star,
  ChevronRight,
  Play,
  Shield
} from 'lucide-react';

const Dashboard: React.FC = () => {
  const [progress, setProgress] = useState<Progress | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const data = await progressAPI.getProgress();
        setProgress(data);
      } catch (error) {
        console.error('Error fetching progress:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-100 via-purple-100 to-blue-100 dark:from-purple-900 dark:via-blue-900 dark:to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-lg text-gray-600 dark:text-gray-300">Loading your cyber adventure...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-100 via-purple-100 to-blue-100 dark:from-purple-900 dark:via-blue-900 dark:to-indigo-900 dark:text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-6">
            <Shield className="h-20 w-20 text-purple-600 animate-pulse" />
          </div>
          <h1 className="text-5xl font-black text-gray-800 dark:text-white mb-4">
            Welcome, Cyber Hero! 🚀
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-6">
            Ready to continue your cybersecurity adventure? No account needed! 🎉
          </p>
          {progress && (
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-6 inline-block">
              <p className="text-lg font-semibold text-gray-800 dark:text-white">{progress.message}</p>
            </div>
          )}
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl p-6 text-white text-center transform hover:scale-105 transition-all duration-300">
            <BookOpen className="h-12 w-12 mx-auto mb-4" />
            <h3 className="text-2xl font-bold">
              {progress?.available_modules || 3} Modules
            </h3>
            <p className="text-purple-100">Learning Adventures</p>
          </div>
          
          <div className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl p-6 text-white text-center transform hover:scale-105 transition-all duration-300">
            <Brain className="h-12 w-12 mx-auto mb-4" />
            <h3 className="text-2xl font-bold">
              {progress?.available_quizzes || 3} Quizzes
            </h3>
            <p className="text-blue-100">Test Your Knowledge</p>
          </div>
          
          <div className="bg-gradient-to-r from-yellow-500 to-orange-500 rounded-2xl p-6 text-white text-center transform hover:scale-105 transition-all duration-300">
            <Trophy className="h-12 w-12 mx-auto mb-4" />
            <h3 className="text-2xl font-bold">Unlimited</h3>
            <p className="text-yellow-100">Fun & Learning</p>
          </div>
        </div>

        {/* Learning Modules */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
            <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-6 flex items-center">
              <BookOpen className="h-8 w-8 mr-3 text-purple-600" />
              Learning Modules 📚
            </h2>
            
            <div className="space-y-4">
              <Link
                to="/modules/password-basics"
                className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-800 dark:to-pink-800 rounded-xl hover:from-purple-200 hover:to-pink-200 dark:hover:from-purple-700 dark:hover:to-pink-700 transition-all duration-300 group"
              >
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center mr-4">
                    <span className="text-2xl">🔐</span>
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-800 dark:text-white">Password Power</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">Create super-strong passwords</p>
                  </div>
                </div>
                <ChevronRight className="h-5 w-5 text-gray-400 group-hover:text-purple-600 transition-colors" />
              </Link>

              <Link
                to="/modules/phishing-awareness"
                className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-100 to-cyan-100 dark:from-blue-800 dark:to-cyan-800 rounded-xl hover:from-blue-200 hover:to-cyan-200 dark:hover:from-blue-700 dark:hover:to-cyan-700 transition-all duration-300 group"
              >
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mr-4">
                    <span className="text-2xl">🕵️</span>
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-800 dark:text-white">Phishing Detective</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">Spot fake emails and websites</p>
                  </div>
                </div>
                <ChevronRight className="h-5 w-5 text-gray-400 group-hover:text-blue-600 transition-colors" />
              </Link>

              <Link
                to="/modules/social-media-safety"
                className="flex items-center justify-between p-4 bg-gradient-to-r from-green-100 to-emerald-100 dark:from-green-800 dark:to-emerald-800 rounded-xl hover:from-green-200 hover:to-emerald-200 dark:hover:from-green-700 dark:hover:to-emerald-700 transition-all duration-300 group"
              >
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center mr-4">
                    <span className="text-2xl">📱</span>
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-800 dark:text-white">Social Media Safety</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">Stay safe on social platforms</p>
                  </div>
                </div>
                <ChevronRight className="h-5 w-5 text-gray-400 group-hover:text-green-600 transition-colors" />
              </Link>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
            <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-6 flex items-center">
              <Target className="h-8 w-8 mr-3 text-blue-600" />
              Quick Actions 🎯
            </h2>
            
            <div className="space-y-4">
              <Link
                to="/quiz/password"
                className="flex items-center p-4 bg-gradient-to-r from-yellow-100 to-orange-100 dark:from-yellow-800 dark:to-orange-800 rounded-xl hover:from-yellow-200 hover:to-orange-200 dark:hover:from-yellow-700 dark:hover:to-orange-700 transition-all duration-300 group"
              >
                <div className="w-12 h-12 bg-yellow-500 rounded-xl flex items-center justify-center mr-4">
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-800 dark:text-white">Take a Quiz</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">Test your knowledge</p>
                </div>
                <Play className="h-5 w-5 text-gray-400 group-hover:text-yellow-600 transition-colors" />
              </Link>

              <Link
                to="/leaderboard"
                className="flex items-center p-4 bg-gradient-to-r from-purple-100 to-indigo-100 dark:from-purple-800 dark:to-indigo-800 rounded-xl hover:from-purple-200 hover:to-indigo-200 dark:hover:from-purple-700 dark:hover:to-indigo-700 transition-all duration-300 group"
              >
                <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center mr-4">
                  <Trophy className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-800 dark:text-white">View Leaderboard</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">See top cyber heroes</p>
                </div>
                <ChevronRight className="h-5 w-5 text-gray-400 group-hover:text-purple-600 transition-colors" />
              </Link>

              <Link
                to="/modules"
                className="flex items-center p-4 bg-gradient-to-r from-pink-100 to-rose-100 dark:from-pink-800 dark:to-rose-800 rounded-xl hover:from-pink-200 hover:to-rose-200 dark:hover:from-pink-700 dark:hover:to-rose-700 transition-all duration-300 group"
              >
                <div className="w-12 h-12 bg-pink-500 rounded-xl flex items-center justify-center mr-4">
                  <Star className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-800 dark:text-white">Browse All Modules</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">Explore all learning content</p>
                </div>
                <ChevronRight className="h-5 w-5 text-gray-400 group-hover:text-pink-600 transition-colors" />
              </Link>
            </div>
          </div>
        </div>

        {/* Fun Fact */}
        <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-2xl p-8 text-white text-center">
          <h2 className="text-3xl font-bold mb-4">🎉 Fun Fact!</h2>
          <p className="text-xl">
            Cybersecurity heroes help protect over 4.6 billion internet users worldwide! 
            You're joining an amazing community of digital defenders! 🛡️
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
