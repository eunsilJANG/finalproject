import React from 'react';
import styled from 'styled-components';
import { useParams, useNavigate } from 'react-router-dom';
import jobsData from '../data/jobs_with_details.json';

// Styled Components 정의
const Container = styled.div`
  max-width: 768px;
  margin: 0 auto;
  background-color: #fff;
`;

const Header = styled.header`
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
`;

const BackButton = styled.button`
  border: none;
  background: none;
  font-size: 24px;
  cursor: pointer;
  padding: 0 16px;
`;

const Title = styled.h1`
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: normal;
  margin: 0;
`;

const ShareButton = styled.button`
  border: none;
  background: none;
  cursor: pointer;
  padding: 0 16px;
`;

const Content = styled.div`
  padding: 0;
`;

const CompanyName = styled.div`
  color: #666;
  font-size: 14px;
  padding: 16px 16px 8px 16px;
`;

const JobTitle = styled.h2`
  font-size: 20px;
  margin: 0;
  padding: 0 16px 16px 16px;
  line-height: 1.4;
`;

const TabContainer = styled.div`
  display: flex;
  padding: 0 16px;
  margin-bottom: 16px;
  gap: 8px;
`;

const Tab = styled.button`
  padding: 6px 12px;
  border: 1px solid #ffe082;
  border-radius: 20px;
  background: #fff;
  font-size: 14px;
  color: #666;
  cursor: pointer;
`;

const Section = styled.section`
  margin-bottom: 16px;
  background: #fff;
`;

const SectionTitle = styled.h3`
  font-size: 15px;
  font-weight: 600;
  padding: 0 20px;
  margin: 0 0 12px;
  position: relative;

  &:after {
    content: '';
    position: absolute;
    left: 20px;
    bottom: -4px;
    width: 50px;
    height: 2px;
    background-color: #ffd338;
  }
`;

const InfoTable = styled.div`
  padding: 0 16px;
`;

const InfoRow = styled.div`
  display: flex;
  padding: 8px 0;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }
`;

const Label = styled.span`
  width: 80px;
  color: #333;
  font-size: 14px;
`;

const Value = styled.span`
  flex: 1;
  color: #333;
  font-size: 14px;
`;

const MapContainer = styled.div`
  margin: 16px;
  height: 200px;
  background: #f5f5f5;
  border-radius: 8px;
`;

const PreferenceSection = styled(Section)`
  margin-top: 8px;
`;

const DetailList = styled.ul`
  list-style: none;
  padding: 0 16px;
  margin: 0;
`;

const DetailItem = styled.li`
  position: relative;
  padding: 8px 0 8px 12px;
  font-size: 14px;
  color: #333;

  &:before {
    content: '-';
    position: absolute;
    left: 0;
  }
`;

const ContactInfo = styled.div`
  padding: 16px;
  background: #fff;
  margin-top: 8px;
`;

const ApplyButton = styled.button`
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: 768px;
  margin: 0 auto;
  padding: 16px;
  background-color: #ffd338;
  color: #333;
  border: none;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
`;

const BookmarkButton = styled.button`
  border: none;
  background: none;
  padding: 8px;
  position: absolute;
  right: 16px;
  bottom: 16px;
  cursor: pointer;
`;

const RegistrationDate = styled.div`
  padding: 8px 16px;
  color: #666;
  font-size: 14px;
  text-align: right;
`;

const URLLink = styled.a`
  color: #0066cc;
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
`;

const JobPostingDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const jobPosting = jobsData.채용공고목록.find((job) => job.채용공고ID === id);
  const details = jobPosting?.상세정보?.세부요건 || [];

  // 세부요건에서 각 카테고리별 정보 추출
  const basicInfo = details[0] || {}; // 경력조건, 학력, 고용형태, 모집인원 등
  const jobTypeInfo = details[1] || {}; // 모집직종 정보
  const workConditionInfo = details[2] || {}; // 임금조건, 근무시간, 사회보험 등
  const applicationInfo = details[3] || {}; // 접수마감일, 전형방법 등
  const qualificationInfo = details[4] || {}; // 자격요건 정보
  const contactInfo = details[5] || {}; // 담당자 정보
  const registrationInfo = details[6] || {}; // 등록 정보

  return (
    <Container>
      <Header>
        <BackButton onClick={() => navigate(-1)}>←</BackButton>
        <Title>공고 정보</Title>
        <ShareButton>공유</ShareButton>
      </Header>

      <Content>
        <RegistrationDate>
          등록일시: {registrationInfo?.['채용공고 등록일시']?.[0] || ''}
        </RegistrationDate>

        <CompanyName>{jobPosting?.회사명}</CompanyName>
        <JobTitle>{jobPosting?.채용제목}</JobTitle>

        <TabContainer>
          <Tab>
            {applicationInfo?.접수마감일?.[0]?.includes('채용시까지')
              ? '채용시까지'
              : '마감일 확인'}
          </Tab>
          <Tab>
            {basicInfo?.학력?.[0]?.includes('무관') ? '학력무관' : '학력필요'}
          </Tab>
          <Tab>
            {basicInfo?.경력조건?.[0]?.includes('무관')
              ? '경력무관'
              : '경력필요'}
          </Tab>
        </TabContainer>

        <Section>
          <SectionTitle>모집요강</SectionTitle>
          <InfoTable>
            <InfoRow>
              <Label>모집직종</Label>
              <Value>{jobTypeInfo?.모집직종?.[0] || ''}</Value>
            </InfoRow>

            <InfoRow>
              <Label>근무시간</Label>
              <Value>
                {workConditionInfo?.근무시간?.[0]?.split('\n')[0] || ''}
              </Value>
            </InfoRow>
            <InfoRow>
              <Label>경력조건</Label>
              <Value>{basicInfo?.경력조건?.[0]?.split('\n')[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>학력</Label>
              <Value>{basicInfo?.학력?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>고용형태</Label>
              <Value>{basicInfo?.고용형태?.[0] || ''}</Value>
            </InfoRow>
          </InfoTable>
        </Section>

        <Section>
          <SectionTitle>근무조건</SectionTitle>
          <InfoTable>
            <InfoRow>
              <Label>임금조건</Label>
              <Value>
                {workConditionInfo?.임금조건?.[0]?.split('\n')[0] || ''}
              </Value>
            </InfoRow>
            <InfoRow>
              <Label>근무예정지</Label>
              <Value>{basicInfo?.근무예정지?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>근무형태</Label>
              <Value>{workConditionInfo?.근무형태?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>사회보험</Label>
              <Value>
                {workConditionInfo?.사회보험?.[0]
                  ?.split('\n')
                  .map((insurance, index) => (
                    <span key={index}>
                      {insurance}
                      {index <
                        workConditionInfo.사회보험[0].split('\n').length - 1 &&
                        ', '}
                    </span>
                  )) || ''}
              </Value>
            </InfoRow>
            <InfoRow>
              <Label>퇴직급여</Label>
              <Value>{workConditionInfo?.퇴직급여?.[0] || ''}</Value>
            </InfoRow>
          </InfoTable>
        </Section>

        <Section>
          <SectionTitle>직무내용</SectionTitle>
          <DetailList>
            {jobPosting?.상세정보?.직무내용
              ?.split('\n')
              .map(
                (line, index) =>
                  line.trim() && <DetailItem key={index}>{line}</DetailItem>
              )}
          </DetailList>
        </Section>

        {/* <Section>
          <SectionTitle>지원자격</SectionTitle>
          <InfoTable>
            {qualificationInfo?.전공?.[0] && (
              <InfoRow>
                <Label>전공</Label>
                <Value>{qualificationInfo.전공[0]}</Value>
              </InfoRow>
            )}
            {qualificationInfo?.자격면허?.[0] !== '관계없음' && (
              <InfoRow>
                <Label>자격면허</Label>
                <Value>{qualificationInfo.자격면허[0]}</Value>
              </InfoRow>
            )}
          </InfoTable>
        </Section> */}

        <Section>
          <SectionTitle>지원방법</SectionTitle>
          <InfoTable>
            <InfoRow>
              <Label>전형방법</Label>
              <Value>{applicationInfo?.전형방법?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>접수방법</Label>
              <Value>{applicationInfo?.접수방법?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>제출서류 준비물</Label>
              <Value>{applicationInfo?.['제출서류 준비물']?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>채용공고 URL</Label>
              <Value>
                <URLLink
                  href={jobPosting?.채용공고URL}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  채용공고 바로가기
                </URLLink>
              </Value>
            </InfoRow>
            <InfoRow>
              <Label>마감일</Label>
              <Value>
                {applicationInfo?.접수마감일?.[0]?.split('\n')[0] || ''}
              </Value>
            </InfoRow>
          </InfoTable>
        </Section>

        <ContactInfo>
          <SectionTitle>채용담당자 정보</SectionTitle>
          <InfoTable>
            <InfoRow>
              <Label>담당자</Label>
              <Value>{contactInfo?.담당자?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>전화번호</Label>
              <Value>{contactInfo?.전화번호?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>휴대폰번호</Label>
              <Value>{contactInfo?.휴대폰번호?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>팩스번호</Label>
              <Value>{contactInfo?.팩스번호?.[0] || ''}</Value>
            </InfoRow>
            <InfoRow>
              <Label>이메일</Label>
              <Value>{contactInfo?.이메일?.[0] || ''}</Value>
            </InfoRow>
          </InfoTable>
        </ContactInfo>

        <ApplyButton
          onClick={() =>
            jobPosting?.채용공고URL &&
            window.open(jobPosting.채용공고URL, '_blank')
          }
        >
          고용24 입사지원
        </ApplyButton>
        <BookmarkButton>☆</BookmarkButton>
      </Content>
    </Container>
  );
};

export default JobPostingDetail;
