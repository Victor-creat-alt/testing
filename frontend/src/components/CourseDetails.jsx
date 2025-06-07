import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CourseDetails.css';
import { useAuth } from '../../contexts/AuthContext';

const CourseDetails = () => {
  const courses = [
    {
      id: 1,
      title: 'Introduction to Python',
      overview: 'Begin your coding journey with Python',
      duration: '8 weeks',
      guidelines: 'Perfect for complete beginners. No prior coding experience required.',
      details: 'Learn the basics of Python including syntax, data types, and control structures',
      image: 'intro-python.jpeg',
    },
    {
      id: 2,
      title: 'Web Development Fundamentals',
      overview: 'Master full-stack development from scratch',
      duration: '12 weeks',
      guidelines: 'Perfect for complete beginners. No prior coding experience required.',
      details: 'Learn HTML5, CSS3, JavaScript ES6+, React, Node.js, Express, and MongoDB through hands-on projects',
      image: 'webdev.jpg',
    },
    {
      id: 3,
      title: 'Data Structures and Algorithms',
      overview: 'Optimize your code and solve complex problems',
      duration: '14 weeks',
      guidelines: 'Basic programming knowledge helpful.',
      details: 'Learn key data structures, algorithms, and their implementation in Python or Java',
      image: 'data-structures.jpeg',
    },
    {
      id: 4,
      title: 'Data Science Essentials',
      overview: 'Become proficient in data analysis and visualization',
      duration: '16 weeks',
      guidelines: 'Basic math knowledge recommended. Python basics helpful but not required.',
      details: 'Covers Python, Pandas, NumPy, Matplotlib, Seaborn, and introductory machine learning concepts',
      image: 'data-analysis.jpg',
    },
    {
      id: 5,
      title: 'Machine Learning Basics',
      overview: 'Start your journey into the world of AI',
      duration: '20 weeks',
      guidelines: 'Strong math background recommended. Python experience helpful.',
      details: 'Introduction to neural networks, TensorFlow, PyTorch, and AI applications',
      image: 'machine-learning.jpeg',
    },
    {
      id: 6,
      title: 'Advanced Java Programming',
      overview: 'Master Java for high-level software development',
      duration: '18 weeks',
      guidelines: 'Intermediate Java knowledge required.',
      details: 'Dive into advanced concepts like multithreading, networking, and design patterns',
      image: 'advanced-java.jpeg',
    },
    {
      id: 7,
      title: 'Network Security',
      overview: 'Secure your systems from cyber threats',
      duration: '12 weeks',
      guidelines: 'Basic networking knowledge helpful.',
      details: 'Learn firewalls, VPNs, intrusion detection systems, and network hardening techniques',
      image: 'network-security.jpg',
    },
    {
      id: 8,
      title: 'Cloud Computing',
      overview: 'Deploy and manage cloud infrastructure',
      duration: '8 weeks',
      guidelines: 'Basic understanding of servers and networking recommended.',
      details: 'Hands-on training with EC2, S3, Lambda, RDS, and other core AWS services',
      image: 'cloud-computing.jpg',
    },
    {
      id: 9,
      title: 'Mobile App Development',
      overview: 'Build cross-platform mobile applications',
      duration: '10 weeks',
      guidelines: 'Basic programming concepts helpful. JavaScript knowledge recommended.',
      details: 'Learn React Native framework to develop iOS and Android apps with single codebase',
      image: 'mobile-app.jpg',
    },
    {
      id: 10,
      title: 'Game Development',
      overview: 'Create immersive games for multiple platforms',
      duration: '18 weeks',
      guidelines: 'Basic programming knowledge helpful.',
      details: 'Learn Unity, C#, game physics, and 3D modeling for game development',
      image: 'game-dev.jpg',
    },
    {
      id: 11,
      title: 'Internet Of Things',
      overview: 'Build interconnected systems and smart devices',
      duration: '12 weeks',
      guidelines: 'Basic programming knowledge and understanding of electronics recommended.',
      details: 'Explore IoT frameworks, sensors, data processing, and smart device applications',
      image: 'iot.jpg',
    },
    {
      id: 12,
      title: 'Blockchain Technology',
      overview: 'Understand blockchain and decentralized apps',
      duration: '12 weeks',
      guidelines: 'Basic programming knowledge recommended.',
      details: 'Learn Ethereum, smart contracts, blockchain security, and cryptocurrency basics',
      image: 'blockchain-technology.jpg',
    },
    {
      id: 13,
      title: 'Computer Graphics Fundamentals',
      overview: 'Design realistic 3D models and animations',
      duration: '14 weeks',
      guidelines: 'Basic math and programming skills recommended.',
      details: 'Explore OpenGL, shaders, rendering techniques, and 3D transformations',
      image: 'computer-graphics.jpeg',
    },
    {
      id: 14,
      title: 'UI/UX Design Principles',
      overview: 'Design intuitive user interfaces',
      duration: '8 weeks',
      guidelines: 'No prior experience needed. Creativity encouraged!',
      details: 'Master Figma, user research, wireframing, prototyping, and design systems',
      image: 'UI-UX.jpg',
    },
    {
      id: 15,
      title: 'DevOps Engineering',
      overview: 'Implement CI/CD pipelines',
      duration: '10 weeks',
      guidelines: 'Basic Linux command line experience recommended.',
      details: 'Learn Docker, Kubernetes, Terraform, GitHub Actions, and infrastructure as code',
      image: 'devops.webp',
    },
    {
      id: 16,
      title: 'Cybersecurity Basics',
      overview: 'Learn to protect systems and networks',
      duration: '14 weeks',
      guidelines: 'Basic computer and networking knowledge required.',
      details: 'Covers ethical hacking, encryption, network security, and security best practices',
      image: 'cybersecurity.jpeg',
    },
    {
      id: 17,
      title: 'Robotics Fundamentals',
      overview: 'Explore the world of robotics',
      duration: '15 weeks',
      guidelines: 'Basic programming and electronics knowledge helpful.',
      details: 'Learn Arduino, Raspberry Pi, sensors, actuators, and robotics algorithms',
      image: 'robotics.jpg',
    },
    {
      id: 18,
      title: 'Advanced C++ Programming',
      overview: 'Develop expertise in C++ for system-level programming',
      duration: '16 weeks',
      guidelines: 'Intermediate C++ knowledge required.',
      details: 'Learn advanced topics like memory management, design patterns, and template programming',
      image: 'advanced-cpp.jpeg',
    },
  ];

  const { authState } = useAuth();
  const userId = authState.studentId;

  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [error, setError] = useState(null);

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://course-2tq7.onrender.com';

  useEffect(() => {
    if (userId) {
      const fetchEnrolledCourses = async () => {
        try {
          const response = await axios.get(
            `${API_BASE_URL}/enrollments?studentId=${userId}`
          );
          const enrolledCourseIds = response.data.map(
            (enrollment) => enrollment.courseId
          );
          setEnrolledCourses(enrolledCourseIds);
          setError(null);
        } catch (err) {
          console.error('Error fetching enrolled courses:', err);
          setError('Failed to fetch enrolled courses.');
        }
      };
      fetchEnrolledCourses();
    }
  }, [userId]);

  const handleToggleEnrollment = async (courseId) => {
    if (!userId) {
      alert('Please log in to enroll in courses.');
      return;
    }
    try {
      if (enrolledCourses.includes(courseId)) {
        // Find the enrollment id to delete
        const response = await axios.get(
          `${API_BASE_URL}/enrollments?studentId=${userId}&courseId=${courseId}`
        );
        const enrollment = response.data[0];
        if (!enrollment) {
          setError('Enrollment not found.');
          return;
        }
        await axios.delete(`${API_BASE_URL}/enrollments/${enrollment.id}`);
        setEnrolledCourses(enrolledCourses.filter((id) => id !== courseId));
        alert('You have been de-enrolled from the course.');
      } else {
        await axios.post(`${API_BASE_URL}/enrollments`, {
          studentId: userId,
          courseId: courseId,
        });
        setEnrolledCourses([...enrolledCourses, courseId]);
        alert('Enrolled successfully.');
      }
      setError(null);
    } catch (err) {
      console.error('Failed to toggle enrollment:', err);
      setError('Failed to toggle enrollment.');
    }
  };

  return (
    <div className="home-container">
      <h1>Welcome to Tech Academy</h1>
      {error && <div className="error">{error}</div>}
      <div className="course-grid">
        {courses.map((course) => {
          const isEnrolled = enrolledCourses.includes(course.id);
          return (
            <div key={course.id} className="course-card">
              <div className="course-image-container">
                <img
                  src={`/assets/${course.image}`}
                  alt={course.title}
                  className="course-image"
                />
              </div>
              <h2>{course.title}</h2>
              <p>
                <strong>Overview:</strong> {course.overview}
              </p>
              <p>
                <strong>Duration:</strong> {course.duration}
              </p>
              <p>
                <strong>For Beginners:</strong> {course.guidelines}
              </p>
              <div className="course-actions">
                <button
                  className={`action-btn ${
                    isEnrolled ? 'enrolled-btn' : 'enroll-btn'
                  }`}
                  onClick={() => handleToggleEnrollment(course.id)}
                >
                  {isEnrolled ? 'Enrolled' : 'Enroll Now'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CourseDetails;
