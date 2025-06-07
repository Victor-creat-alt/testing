import React, { useState, useEffect } from "react";
import { Pie, Line } from "react-chartjs-2";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Chart, registerables } from "chart.js";
import axios from "axios";
import "./Dashboard.css";
import DashboardBarGraph from './DashboardBarGraph';
import { FiLogOut } from 'react-icons/fi'; // Import the logout icon

Chart.register(...registerables);

const Dashboard = () => {
    const [courses, setCourses] = useState([]);
    const [studentProgress, setStudentProgress] = useState([]);
    const [selectedCourse, setSelectedCourse] = useState(null);
    const [enrollmentsData, setEnrollmentsData] = useState([]);
    const [instructors, setInstructors] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [isDarkMode, setIsDarkMode] = useState(false);
    const API_BASE_URL = import.meta.env.VITE_API_URL || "";
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const coursesResponse = await axios.get(API_BASE_URL + "/courses");
                if (coursesResponse.headers["content-type"] && coursesResponse.headers["content-type"].includes("application/json")) {
                    // Prepend API_BASE_URL to image_url if relative
                    const coursesData = coursesResponse.data.map(course => {
                        let imageUrl = course.image_url || "";
                        if (imageUrl && !imageUrl.startsWith("http://") && !imageUrl.startsWith("https://")) {
                            imageUrl = API_BASE_URL + imageUrl;
                        }
                        return { ...course, image_url: imageUrl };
                    });
                    setCourses(coursesData);
                } else {
                    console.error("Courses data is not JSON:", coursesResponse);
                    setCourses([]);
                }

                const studentsResponse = await axios.get(API_BASE_URL + "/students");
                if (studentsResponse.headers["content-type"] && studentsResponse.headers["content-type"].includes("application/json")) {
                    const progressData = Array.isArray(studentsResponse.data)
                        ? studentsResponse.data.map((student) => ({
                            course: Array.isArray(student.courses) && student.courses.length > 0
                                ? student.courses.map((course) => course.title).join(", ")
                                : "No Courses Available",
                            progress: Array.isArray(student.enrollments)
                                ? student.enrollments.length
                                : 0,
                            name: student.name,
                        }))
                        : [];
                    setStudentProgress(progressData);
                } else {
                    console.error("Students data is not JSON:", studentsResponse);
                    setStudentProgress([]);
                }

                const enrollmentsResponse = await axios.get(API_BASE_URL + "/enrollments");
                if (enrollmentsResponse.headers["content-type"] && enrollmentsResponse.headers["content-type"].includes("application/json")) {
                    const enrollments = Array.isArray(enrollmentsResponse.data)
                        ? enrollmentsResponse.data.map((enrollment) => ({
                            studentName: enrollment.student?.name || "Unknown",
                            courseTitle: enrollment.course?.title || "Unknown Course",
                            grade: enrollment.grade || "0",
                        }))
                        : [];
                    setEnrollmentsData(enrollments);
                } else {
                    console.error("Enrollments data is not JSON:", enrollmentsResponse);
                    setEnrollmentsData([]);
                }

                const instructorsResponse = await axios.get(API_BASE_URL + "/instructors");
                if (instructorsResponse.headers["content-type"] && instructorsResponse.headers["content-type"].includes("application/json")) {
                    setInstructors(instructorsResponse.data);
                } else {
                    console.error("Instructors data is not JSON:", instructorsResponse);
                    setInstructors([]);
                }

                const departmentsResponse = await axios.get(API_BASE_URL + "/departments");
                if (departmentsResponse.headers["content-type"] && departmentsResponse.headers["content-type"].includes("application/json")) {
                    setDepartments(departmentsResponse.data);
                } else {
                    console.error("Departments data is not JSON:", departmentsResponse);
                    setDepartments([]);
                }
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
    }, []);

    // Process instructors data to get counts of instructors per course and their department allocations
    // Structure: { courseTitle: { departmentName: count } }
    const courseDeptInstructorCounts = {};
    instructors.forEach(instructor => {
        if (Array.isArray(instructor.courses)) {
            instructor.courses.forEach(course => {
                const courseTitle = course.title || "Unknown Course";
                const departmentName = instructor.department?.name || "Unknown Department";
                if (!courseDeptInstructorCounts[courseTitle]) {
                    courseDeptInstructorCounts[courseTitle] = {};
                }
                if (!courseDeptInstructorCounts[courseTitle][departmentName]) {
                    courseDeptInstructorCounts[courseTitle][departmentName] = 0;
                }
                courseDeptInstructorCounts[courseTitle][departmentName] += 1;
            });
        }
    });

    // Prepare data for line graph
    const lineLabels = Object.keys(courseDeptInstructorCounts);
    const departmentNames = [...new Set(instructors.map(inst => inst.department?.name || "Unknown Department"))];

    const datasets = departmentNames.map((deptName, index) => {
        return {
            label: deptName,
            data: lineLabels.map(courseTitle => courseDeptInstructorCounts[courseTitle][deptName] || 0),
            fill: false,
            borderColor: "hsl(" + ((index * 60) % 360) + ", 70%, 50%)",
            tension: 0.1,
        };
    });

    const lineGraphData = {
        labels: lineLabels,
        datasets: datasets,
    };

    const lineGraphOptions = {
        responsive: true,
        plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Instructors Assigned to Courses by Department' },
        },
        scales: {
            y: { beginAtZero: true, title: { display: true, text: 'Number of Instructors' } },
            x: { title: { display: true, text: 'Courses' } },
        },
    };

    const coursePieData = {
        labels: courses.map((course) => course.title),
        datasets: [
            {
                data: courses.map((course) => parseInt(course.duration, 10) || 0),
                backgroundColor: [
                    "rgba(255, 99, 132, 0.6)",
                    "rgba(54, 162, 235, 0.6)",
                    "rgba(255, 206, 86, 0.6)",
                    "rgba(75, 192, 192, 0.6)",
                    "rgba(153, 102, 255, 0.6)",
                    "rgba(255, 159, 64, 0.6)",
                ],
                borderColor: [
                    "rgba(255, 99, 132, 1)",
                    "rgba(54, 162, 235, 1)",
                    "rgba(255, 206, 86, 1)",
                    "rgba(75, 192, 192, 1)",
                    "rgba(153, 102, 255, 1)",
                    "rgba(255, 159, 64, 1)",
                ],
                borderWidth: 1,
            },
        ],
    };

    const handleViewDetails = (course) => {
        setSelectedCourse(course);
    };

    const handleCloseDetails = () => {
        setSelectedCourse(null);
    };

    const toggleTheme = () => {
        setIsDarkMode(!isDarkMode);
    };

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        sessionStorage.clear();
        navigate('/login', { state: { userType: 'instructor' } });
    };

    const uniqueCourses = [...new Set(enrollmentsData.map(item => item.courseTitle))];
    const barGraphData = uniqueCourses.map(courseTitle => {
        const filteredEnrollments = enrollmentsData.filter(item => item.courseTitle === courseTitle);
        const enrollmentCount = filteredEnrollments.length;
        const averageGrade = filteredEnrollments.reduce((acc, item) => acc + (parseInt(item.grade) || 0), 0) / enrollmentCount || 0;
        return { courseTitle, enrollmentCount, averageGrade };
    });

    return (
        <div className={"dashboard-container " + (isDarkMode ? "dark-mode" : "light-mode")}>
            <div className="navigation-links">
                <Link to="/dashboard" className={location.pathname === "/dashboard" ? "active" : ""}>Dashboard</Link>
                <Link to="/departments" className={location.pathname === "/departments" ? "active" : ""}>Departments</Link>
                <Link to="/students" className={location.pathname === "/students" ? "active" : ""}>Students</Link>
                <Link to='/enrolled-students' className={location.pathname === "/enrolled-students" ? "active" : ""}>Enrolled Students</Link>
                <button className="logout-button" onClick={handleLogout} aria-label="Logout">
                    <FiLogOut />
                </button>
            </div>
            <button className="theme-toggle-button" onClick={toggleTheme}>
                Switch to {isDarkMode ? "Light Mode" : "Dark Mode"}
            </button>
            <div className="line-graph-section">
                <h2>Instructors Assigned to Courses by Department</h2>
                {lineLabels.length > 0 ? (
                    <Line data={lineGraphData} options={lineGraphOptions} />
                ) : (
                    <p>Loading instructor assignment data...</p>
                )}
            </div>
            <div className="progress-section">
                <h2>Course Durations</h2>
                <Pie data={coursePieData} options={{ responsive: true }} />
            </div>
            <div className="progress-section-2">
                <h2>Enrollments and Grades by Course</h2>
                {barGraphData.length > 0 ? (
                    <DashboardBarGraph data={barGraphData} />
                ) : (
                    <p>Loading enrollment data...</p>
                )}
            </div>
            {selectedCourse && (
                <div className="course-details-modal" role="dialog" aria-modal="true" aria-labelledby="course-details-title">
                    <div className="course-details-content">
                        <h3 id="course-details-title">{selectedCourse.title}</h3>
                        <p>{selectedCourse.description}</p>
                        <button onClick={handleCloseDetails}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
