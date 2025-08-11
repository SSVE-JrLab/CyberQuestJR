import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { userAPI } from '../services/api';
import { UserCreate } from '../types';
import { User, Sparkles, ArrowRight } from 'lucide-react';

const UserProfile = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<UserCreate>({
    name: '',
    age: 8,
    experience_level: 'beginner',
    interests: []
  });
  const [loading, setLoading] = useState(false);
  const [userId, setUserId] = useState<number | null>(
    localStorage.getItem('cyberquest_user_id') ?
    parseInt(localStorage.getItem('cyberquest_user_id')!) : null
  );

  const experienceLevels = [
    { value: 'beginner', label: 'Beginner - New to computers and internet' },
    { value: 'intermediate', label: 'Intermediate - I know the basics' },
    { value: 'advanced', label: 'Advanced - I\'m comfortable with technology' }
  ];

  const interestOptions = [
    'Gaming', 'Social Media', 'Online Learning', 'Videos & Streaming',
    'Shopping Online', 'Messaging Friends', 'Creating Content', 'Programming'
  ];

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await userAPI.createUser(formData);
      localStorage.setItem('cyberquest_user_id', response.id.toString());
      localStorage.setItem('cyberquest_user_name', response.name);
      setUserId(response.id);
      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to create user:', error);
      alert('Failed to create profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = () => {
    if (userId) {
      navigate('/dashboard');
    }
  };

  if (userId) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-purple-900 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
          <div className="mb-6">
            <div className="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mx-auto mb-4">
              <User className="w-8 h-8 text-green-600 dark:text-green-400" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Welcome back, {localStorage.getItem('cyberquest_user_name')}!
            </h2>
            <p className="text-gray-600 dark:text-gray-300">
              Ready to continue your cybersecurity journey?
            </p>
          </div>

          <button
            onClick={handleContinue}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            Continue Learning
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-purple-900 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mx-auto mb-4">
            <Sparkles className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Create Your CyberQuest Profile
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Tell us about yourself so we can create the perfect learning experience!
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              What's your name?
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your name"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              How old are you?
            </label>
            <input
              type="number"
              min="6"
              max="18"
              value={formData.age}
              onChange={(e) => setFormData(prev => ({ ...prev, age: parseInt(e.target.value) }))}
              className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              What's your experience with computers and internet?
            </label>
            <div className="space-y-2">
              {experienceLevels.map((level) => (
                <label key={level.value} className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    name="experience_level"
                    value={level.value}
                    checked={formData.experience_level === level.value}
                    onChange={(e) => setFormData(prev => ({ ...prev, experience_level: e.target.value }))}
                    className="mr-3 text-blue-600"
                  />
                  <span className="text-gray-700 dark:text-gray-300">{level.label}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              What do you like to do online? (Select all that apply)
            </label>
            <div className="grid grid-cols-2 gap-2">
              {interestOptions.map((interest) => (
                <label key={interest} className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.interests.includes(interest)}
                    onChange={() => handleInterestToggle(interest)}
                    className="mr-2 text-blue-600"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300">{interest}</span>
                </label>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !formData.name.trim()}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>Creating Profile...</>
            ) : (
              <>
                Start Learning
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default UserProfile;
