import React, { useState, useEffect } from 'react';
import Modal from './page/Modal';

const Home = () => {
  const [cards, setCards] = useState([]); // 전체 공고 데이터
  const [filteredCards, setFilteredCards] = useState([]); // 검색된 공고 데이터
  const [currentCardIndex, setCurrentCardIndex] = useState(0); // 현재 표시되는 카드 인덱스
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
    setCurrentCardIndex(0); // 검색어가 바뀌면 첫 번째 결과부터 보여줌
  };

  const handleDetail = (card) => {
    setModalContent(card); // Modal에 카드 상세 내용 전달
  };

  const handleCloseModal = () => {
    setModalContent(null); // Modal 닫기
  };

  const handleNextCard = () => {
    if (currentCardIndex < filteredCards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1); // 다음 카드로 이동
    } else {
      alert('더 이상 공고가 없습니다.');
    }
  };

  const handlePrevCard = () => {
    if (currentCardIndex > 0) {
      setCurrentCardIndex(currentCardIndex - 1); // 이전 카드로 이동
    } else {
      alert('처음 공고입니다.');
    }
  };

  const currentCard = filteredCards[currentCardIndex];

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f9f9f9',
        padding: '20px',
        minHeight: '100vh',
      }}
    >
      <h1 style={{ marginBottom: '20px', fontSize: '30px', color: '#333' }}>
        맞춤형 일자리
      </h1>

      {/* 검색창 */}
      <div
        style={{
          width: '100%',
          maxWidth: '400px',
          margin: '30px',
        }}
      >
        <input
          type="text"
          placeholder="검색어를 입력하세요 (예: 경비, 주방)"
          value={searchQuery}
          onChange={handleSearchChange}
          style={{
            width: '100%',
            padding: '12px',
            fontSize: '18px',
            borderRadius: '5px',
            border: '1px solid #ddd',
          }}
        />
      </div>

      {/* 카드 영역 */}
      {currentCard ? (
        <div
          style={{
            width: '400px',
            padding: '20px',
            backgroundColor: '#ffffff',
            borderRadius: '10px',
            boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
            textAlign: 'center',
            fontSize: '36px',
          }}
        >
          <h3 style={{ fontSize: '30px', marginBottom: '10px' }}>
            {currentCard.title}
          </h3>

          <p style={{ fontSize: '20px', color: '#777' }}>
            {currentCard.location || '정보 없음'}
          </p>
          <button
            onClick={() => handleDetail(currentCard)}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              marginTop: '20px',
            }}
          >
            상세보기
          </button>
        </div>
      ) : (
        <p style={{ fontSize: '18px', color: '#999', textAlign: 'center' }}>
          검색 결과가 없습니다.
        </p>
      )}

      {/* 이전/다음 공고 보기 버튼 */}
      <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
        <button
          onClick={handlePrevCard}
          style={{
            padding: '10px 30px',
            fontSize: '20px',
            backgroundColor: '#ffc107',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          이전 공고 보기
        </button>
        <button
          onClick={handleNextCard}
          style={{
            padding: '10px 30px',
            fontSize: '20px',
            backgroundColor: '#1dd1a1',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          다음 공고 보기
        </button>
      </div>

      <Modal content={modalContent} onClose={handleCloseModal} />
    </div>
  );
};

export default Home;
