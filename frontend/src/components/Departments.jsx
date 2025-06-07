import React, { useState, useEffect } from 'react';
import axios from 'axios';
import BarChart from './BarChart'; // Import the BarChart component
import DepartmentForm from './DepartmentForm';
import { useNavigate } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa'; // Importing the navigation arrow icon
import './Departments.css';

function Departments() {
  const [departments, setDepartments] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState(null);
  const API_BASE_URL = import.meta.env.VITE_API_URL;
  const navigate = useNavigate();

  const handleBackClick = () => {
    navigate('/dashboard'); // Navigate back to Dashboard.jsx
  };

  useEffect(() => {
    if (!API_BASE_URL) {
      setError('API base URL is not defined. Please check your environment configuration.');
      return;
    }
    axios.get(API_BASE_URL + '/departments')
      .then(res => {
        if (res.headers['content-type'] && res.headers['content-type'].includes('application/json')) {
          setDepartments(res.data || []);
          setError(null);
        } else {
          console.error('Departments data is not JSON:', res);
          setDepartments([]);
          setError('Received data is not in JSON format.');
        }
      })
      .catch(error => {
        console.error('Error fetching departments:', error);
        setError('Failed to fetch departments. Please try again later.');
        setDepartments([]);
      });
  }, [API_BASE_URL]);

  const handleAddDepartment = (newDepartment) => {
    if (!API_BASE_URL) {
      setError('API base URL is not defined. Cannot add department.');
      return;
    }
    axios.post(API_BASE_URL + '/departments', newDepartment)
      .then(res => {
        setDepartments([...departments, res.data]);
        setIsModalOpen(false);
        setError(null);
      })
      .catch(error => {
        console.error('Error adding department:', error);
        setError('Failed to add department. Please try again.');
      });
  };

  const handleDeleteDepartment = (id) => {
    if (!API_BASE_URL) {
      setError('API base URL is not defined. Cannot delete department.');
      return;
    }
    axios.delete(API_BASE_URL + '/departments/' + id)
      .then(() => {
        setDepartments((departments || []).filter(department => department.id !== id));
        setError(null);
      })
      .catch(error => {
        console.error('Error deleting department:', error);
        setError('Failed to delete department. Please try again.');
      });
  };

  const filteredDepartments = (departments || []).filter(department =>
    department?.name?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div>
      <h1>Departments</h1>
      <button className="add-department-button" onClick={() => setIsModalOpen(true)}>
        Add Department
      </button>
      <button onClick={handleBackClick} className="back-button">
        <FaArrowLeft />
      </button>

      {isModalOpen && (
        <DepartmentForm 
          onClose={() => setIsModalOpen(false)} 
          onSubmit={handleAddDepartment} 
        />
      )}

      <input
        type="text"
        placeholder="Search departments..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className="search-input"
      />

      {error ? (
        <p className="error-message" style={{ color: 'red' }}>{error}</p>
      ) : (departments && departments.length > 0) ? (
        <>
          <table className="departments-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Location</th>
                <th>Head</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredDepartments.map(department => (
                <tr key={department.id}>
                  <td>{department.name}</td>
                  <td>{department.location}</td>
                  <td>{department.head}</td>
                  <td>
                    <button 
                      className="delete-button" 
                      onClick={() => handleDeleteDepartment(department.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <BarChart departments={departments} /> {/* Render the bar chart */}
        </>
      ) : (
        <p>Loading departments...</p>
      )}
    </div>
  );
}

export default Departments;
