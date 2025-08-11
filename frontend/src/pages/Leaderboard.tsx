import { useState, useEffect } from 'react';
import { leaderboardAPI } from '../services/api';
import { LeaderboardEntry } from '../types';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    try {
      const data = await leaderboardAPI.getLeaderboard();
      setLeaderboard(data.leaderboard || []);
    } catch (error) {
      console.error('Failed to load leaderboard:', error);
      setLeaderboard([]);
    } finally {
      setLoading(false);
    }
  };

  const getBadge = (index: number): string => {
    switch (index) {
      case 0: return '👑';
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return '⭐';
    }
  };

  const getLevel = (averageScore: number): string => {
    if (averageScore >= 90) return 'Expert';
    if (averageScore >= 80) return 'Advanced';
    if (averageScore >= 70) return 'Intermediate';
    return 'Beginner';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-purple-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-purple-900 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            🏆 Leaderboard
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            See how you rank among other cybersecurity learners!
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
          {leaderboard.length > 0 ? (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {leaderboard.map((entry, index) => (
                <div key={index} className="p-6 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="text-3xl">{getBadge(index)}</div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          {entry.name}
                        </h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          Level: {getLevel(entry.average_score)}
                        </p>
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="flex items-center space-x-6">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                            {entry.completed_courses}
                          </div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">Courses</div>
                        </div>

                        <div className="text-center">
                          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                            {Math.round(entry.average_score)}%
                          </div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">Avg Score</div>
                        </div>

                        {entry.has_certificate && (
                          <div className="text-center">
                            <div className="text-2xl">🎓</div>
                            <div className="text-xs text-gray-500 dark:text-gray-400">Certified</div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-12 text-center">
              <div className="text-6xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Be the first on the leaderboard!
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Complete courses and quizzes to see your ranking here.
              </p>
            </div>
          )}
        </div>

        {/* Achievement Levels */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">🌱</div>
            <div className="font-semibold text-gray-900 dark:text-white">Beginner</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">0-69% avg</div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">📚</div>
            <div className="font-semibold text-gray-900 dark:text-white">Intermediate</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">70-79% avg</div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">🚀</div>
            <div className="font-semibold text-gray-900 dark:text-white">Advanced</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">80-89% avg</div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">⭐</div>
            <div className="font-semibold text-gray-900 dark:text-white">Expert</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">90%+ avg</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
