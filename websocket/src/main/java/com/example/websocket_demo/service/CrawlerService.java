package com.example.websocket_demo.service;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.springframework.stereotype.Service;


@Service
public class CrawlerService {


    // 크롤링 함수
    public String crawlData() {
        try {
            // 예시 URL
            String url = "https://kr.indeed.com/q-%EA%B3%A0%EB%A0%B9%EC%9E%90-%EC%B1%84%EC%9A%A9%EA%B3%B5%EA%B3%A0.html";
            Document doc = Jsoup.connect(url).get();

            // 예시: 특정 div에서 데이터를 추출
            Element dataElement = doc.select("div.data-class").first();
            if (dataElement != null) {
                return "크롤링된 데이터: " + dataElement.text();
            } else {
                return "데이터를 찾을 수 없습니다.";
            }
        } catch (Exception e) {
            e.printStackTrace();
            return "크롤링 중 오류 발생";
        }
    }


}
