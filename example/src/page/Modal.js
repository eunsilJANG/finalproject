import React from 'react';

const Modal = ({ content, onClose }) => {
  if (!content) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: '0',
        left: '0',
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
      }}
    >
      <div
        style={{
          width: '400px',
          padding: '20px', 
          backgroundColor: 'white',
          borderRadius: '10px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          textAlign: 'left',
          overflowY: 'auto',
          maxHeight: '80vh',
        }}
      >
        {/* 공고 제목 */}
        <h3>{content.title}</h3>

        {/* 회사명 */}

        {/* 위치 */}
        <p>
          <strong>회사명 & 위치:</strong> {content.location || '정보 없음'}
        </p>

        {/* 공고 링크 */}
        <p>
          <strong>공고 링크:</strong>{' '}
          <a
            href={content.link}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#3498db', textDecoration: 'underline' }}
          >
            여기로 이동
          </a>
        </p>

        {/* 상세 내용 (JSON에 detail 필드가 포함된 경우) */}
        {content.detail && (
          <pre
            style={{
              whiteSpace: 'pre-wrap',
              wordWrap: 'break-word',
              marginTop: '20px',
            }}
          >
            {content.detail}
          </pre>
        )}

        {/* 닫기 버튼 */}
        <button
          onClick={onClose}
          style={{
            marginTop: '20px',
            padding: '10px 20px',
            backgroundColor: '#ff6b6b',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          닫기
        </button>
      </div>
    </div>
  );
};

export default Modal;
