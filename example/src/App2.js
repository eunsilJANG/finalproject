import React, { useState, useEffect } from 'react';
import Modal from './page/Modal';
import './assets/css/swiper.css';

const Home = () => {
  const [cards, setCards] = useState([]); // 전체 공고 데이터
  const [filteredCards, setFilteredCards] = useState([]); // 검색된 공고 데이터
  const [searchQuery, setSearchQuery] = useState(''); // 검색어 상태
  const [modalContent, setModalContent] = useState(null);

  // JSON 파일 데이터 불러오기
  useEffect(() => {
    fetch('/jobs.json') // 크롤링한 JSON 파일 경로
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch jobs data');
        }
        return response.json();
      })
      .then((data) => {
        setCards(data);
        setFilteredCards(data); // 초기에는 전체 데이터를 보여줌
      })
      .catch((error) => console.error('Error loading jobs data:', error));
  }, []);

  // 검색어 입력 핸들러
  const handleSearchChange = (e) => {
    const query = e.target.value.toLowerCase();
    setSearchQuery(query);

    // 검색어에 해당하는 공고 필터링
    const filtered = cards.filter(
      (card) =>
        card.title.toLowerCase().includes(query) ||
        card.company?.toLowerCase().includes(query) ||
        card.location?.toLowerCase().includes(query)
    );
    setFilteredCards(filtered);
  };

  const handleDetail = (card) => {
    setModalContent(card); // Modal에 카드 상세 내용 전달
  };

  const handleCloseModal = () => {
    setModalContent(null); // Modal 닫기
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: '100%',
        backgroundColor: '#fafafa',
        padding: '20px',
        boxSizing: 'border-box',
        overflowY: 'scroll', // 스크롤 가능하도록 설정
        height: '100vh', // 전체 화면 높이
      }}
    >
      <h1 style={{ marginBottom: '20px' }}>맞춤형 일자리</h1>

      {/* 검색창 */}
      <section
        style={{
          width: '100%',
          maxWidth: '400px',
          textAlign: 'center',
          marginBottom: '20px',
        }}
      >
        <h2 style={{ marginBottom: '10px' }}>공고 검색</h2>
        <input
          type="text"
          placeholder="검색어를 입력하세요 (예: 경비, 미아동)"
          value={searchQuery}
          onChange={handleSearchChange}
          style={{
            width: '100%',
            padding: '10px',
            fontSize: '16px',
            borderRadius: '5px',
            border: '1px solid #ddd',
            marginBottom: '20px',
          }}
        />
      </section>

      {/* 검색 결과 */}
      <section
        style={{
          width: '100%',
          maxWidth: '600px',
          backgroundColor: '#ffffff',
          borderRadius: '10px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          padding: '20px',
          boxSizing: 'border-box',
          overflowY: 'auto', // 리스트 내부 스크롤
          maxHeight: '70vh', // 리스트 높이 제한
        }}
      >
        {filteredCards.length > 0 ? (
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {filteredCards.map((card, index) => (
              <li
                key={index}
                style={{
                  marginBottom: '20px',
                  padding: '10px',
                  borderBottom: '1px solid #ddd',
                }}
              >
                <h3>{card.title}</h3>
                <p>
                  {card.company || '회사명 없음'} -{' '}
                  {card.location || '위치 정보 없음'}
                </p>
                <button
                  onClick={() => handleDetail(card)}
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
        ) : (
          <p style={{ textAlign: 'center' }}>검색 결과가 없습니다.</p>
        )}
      </section>

      <Modal content={modalContent} onClose={handleCloseModal} />
    </div>
  );
};

export default Home;
