import React, { useState, useEffect } from 'react';
import Modal from './Modal';

const App = () => {
  const [modalContent, setModalContent] = useState(null);
  const [jobData, setJobData] = useState([]); // 크롤링 데이터를 관리할 상태

  // 크롤링 데이터 불러오기
  useEffect(() => {
    fetch('public/jobs.json') // 실제 크롤링 데이터를 저장한 JSON 파일 경로
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => setJobData(data)) // 데이터를 상태로 설정
      .catch((error) => console.error('Error fetching the jobs:', error));
  }, []);

  const handleDetail = (job) => {
    setModalContent(job); // 선택된 공고를 Modal로 전달
  };

  const handleCloseModal = () => {
    setModalContent(null); // Modal 닫기
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>일자리 공고</h1>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {jobData.map((job, index) => (
          <li
            key={index}
            style={{
              marginBottom: '20px',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '10px',
            }}
          >
            <h3>{job.title}</h3>
            <p>{job.location}</p>
            <a href={job.link} target="_blank" rel="noopener noreferrer">
              공고 링크
            </a>
            <button
              onClick={() => handleDetail(job)}
              style={{
                padding: '10px 20px',
                backgroundColor: '#3498db',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
              }}
            >
              상세보기
            </button>
          </li>
        ))}
      </ul>
      <Modal content={modalContent} onClose={handleCloseModal} />
    </div>
  );
};

export default App;
