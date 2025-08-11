import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Shield, BookOpen, Star, Users, Trophy, Clock } from 'lucide-react';

interface Course {
  id: string;
  title: string;
  description: string;
  icon: string;
  level: string;
  difficulty: number;
  estimatedTime: string;
}

const Learn = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  const predefinedCourses: Course[] = [
    {
      id: "password-basics",
      title: "Password Heroes",
      description: "Learn to create super strong passwords that protect your digital world like a superhero shield!",
      icon: "🔐",
      level: "Beginner",
      difficulty: 1,
      estimatedTime: "15 min"
    },
    {
      id: "phishing-awareness",
      title: "Phishing Detective",
      description: "Become an expert detective at spotting fake emails and suspicious messages that try to trick you!",
      icon: "🕵️",
      level: "Beginner",
      difficulty: 1,
      estimatedTime: "20 min"
    },
    {
      id: "digital-footprints",
      title: "Digital Footprint Tracker",
      description: "Understand what traces you leave online and how to manage them like a pro!",
      icon: "👣",
      level: "Intermediate",
      difficulty: 2,
      estimatedTime: "25 min"
    },
    {
      id: "social-media-safety",
      title: "Safe Social Media",
      description: "Navigate social platforms safely and responsibly while having fun with friends!",
      icon: "📱",
      level: "Intermediate",
      difficulty: 2,
      estimatedTime: "30 min"
    },
    {
      id: "cyber-bullying",
      title: "Cyber Bullying Defense",
      description: "Learn to identify, prevent, and respond to online bullying like a true cyber warrior!",
      icon: "🛡️",
      level: "Intermediate",
      difficulty: 2,
      estimatedTime: "25 min"
    },
    {
      id: "privacy-guardian",
      title: "Privacy Guardian",
      description: "Master the art of protecting your personal information and privacy online!",
      icon: "🔒",
      level: "Advanced",
      difficulty: 3,
      estimatedTime: "35 min"
    }
  ];

  useEffect(() => {
    // Simulate loading and set predefined courses
    setTimeout(() => {
      setCourses(predefinedCourses);
      setLoading(false);
    }, 500);
  }, []);

  const getDifficultyStars = (difficulty: number) => {
    return Array(3).fill(0).map((_, i) => (
      <Star
        key={i}
        className={`h-4 w-4 ${i < difficulty ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
      />
    ));
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'Beginner': return 'bg-green-100 text-green-800';
      case 'Intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'Advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-purple-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">Loading awesome courses...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-purple-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-6">
            <div className="relative">
              <BookOpen className="h-16 w-16 text-primary-600 animate-pulse" />
              <Shield className="h-8 w-8 text-yellow-400 absolute -top-1 -right-1" />
            </div>
          </div>

          <h1 className="text-5xl md:text-6xl font-black mb-4 bg-gradient-to-r from-primary-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            🎓 Learn Cybersecurity!
          </h1>

          <p className="text-xl md:text-2xl text-gray-700 dark:text-gray-300 mb-6 max-w-3xl mx-auto">
            Choose your adventure! Each course uses AI to create personalized content just for you! 🤖✨
          </p>

          <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-600 dark:text-gray-400">
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              <span>Perfect for ages 8-18</span>
            </div>
            <div className="flex items-center gap-2">
              <Trophy className="h-4 w-4" />
              <span>Earn certificates</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              <span>Learn at your pace</span>
            </div>
          </div>
        </div>

        {/* Courses Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {courses.map((course) => (
            <Link
              key={course.id}
              to={`/course/${course.id}`}
              className="group block"
            >
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden border border-gray-100 dark:border-gray-700">

                {/* Course Header */}
                <div className="bg-gradient-to-r from-primary-500 to-purple-600 p-6 text-center">
                  <div className="text-6xl mb-3">{course.icon}</div>
                  <h3 className="text-2xl font-bold text-white mb-2">{course.title}</h3>
                  <div className="flex justify-center items-center gap-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getLevelColor(course.level)}`}>
                      {course.level}
                    </span>
                  </div>
                </div>

                {/* Course Content */}
                <div className="p-6">
                  <p className="text-gray-600 dark:text-gray-300 mb-4 leading-relaxed">
                    {course.description}
                  </p>

                  {/* Course Stats */}
                  <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center gap-1">
                      <span className="text-sm text-gray-500 mr-2">Difficulty:</span>
                      {getDifficultyStars(course.difficulty)}
                    </div>
                    <div className="flex items-center gap-1 text-sm text-gray-500">
                      <Clock className="h-4 w-4" />
                      <span>{course.estimatedTime}</span>
                    </div>
                  </div>

                  {/* Start Button */}
                  <button className="w-full bg-gradient-to-r from-primary-600 to-purple-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-primary-700 hover:to-purple-700 transition-all duration-200 transform group-hover:scale-105 shadow-lg">
                    🚀 Start Learning!
                  </button>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Footer Message */}
        <div className="text-center mt-16">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 max-w-3xl mx-auto">
            <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">
              🤖 Powered by AI Magic!
            </h3>
            <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
              Each course is generated by Google Gemini AI to create personalized content based on your age and interests.
              Complete quizzes to test your knowledge and earn awesome certificates! 🏆
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Learn;
