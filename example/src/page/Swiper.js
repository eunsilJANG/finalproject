import React from 'react';
import { useSwipeable } from 'react-swipeable';

const SwipeableCard = ({ content, onDetail }) => {
  const handlers = useSwipeable({
    onSwipedLeft: () => {}, // 스와이프 기능 비활성화
    onSwipedRight: () => {},
  });

  return (
    <div
      {...handlers}
      style={{
        width: '300px',
        height: '400px',
        margin: '20px auto',
        backgroundColor: '#f0f0f0',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: '10px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        position: 'relative',
      }}
    >
      <h3>{content.title}</h3>
      <p>{content.summary}</p>
      <button
        onClick={() => onDetail(content)}
        style={{
          position: 'absolute',
          bottom: '20px',
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
    </div>
  );
};

export default SwipeableCard;
