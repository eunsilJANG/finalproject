import React from 'react';

const ActionButtons = ({ onLeftAction, onRightAction, onUndo }) => {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        width: '300px',
        margin: '20px auto',
      }}
    >
      <button
        onClick={onLeftAction}
        style={{
          padding: '10px 20px',
          backgroundColor: '#ff6b6b',
          border: 'none',
          color: 'white',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        싫어요
      </button>
      <button
        onClick={onUndo}
        style={{
          padding: '10px 20px',
          backgroundColor: '#3498db',
          border: 'none',
          color: 'white',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        되돌리기
      </button>
      <button
        onClick={onRightAction}
        style={{
          padding: '10px 20px',
          backgroundColor: '#1dd1a1',
          border: 'none',
          color: 'white',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        좋아요
      </button>
    </div>
  );
};

export default ActionButtons;
