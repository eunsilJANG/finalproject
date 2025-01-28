package com.example.websocket_demo.service;
import com.example.websocketdemo.handler.CrawlerWebSocketHandler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.socket.WebSocketSession;

import java.io.IOException;
import java.util.List;

@Service
public class CrawlerSchedulerService {

    @Autowired
    private CrawlerService crawlerService;

    @Autowired
    private CrawlerWebSocketHandler webSocketHandler;

    private List<WebSocketSession> sessions; // 모든 연결된 세션

    // 10초마다 크롤링 작업을 실행하고 모든 클라이언트에 전송
    @Scheduled(fixedRate = 10000)
    public void sendCrawledDataToClients() {
        String crawledData = crawlerService.crawlData();
        for (WebSocketSession session : sessions) {
            try {
                webSocketHandler.sendCrawledData(session, crawledData);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // 새로운 세션을 추가하는 메서드
    public void addSession(WebSocketSession session) {
        sessions.add(session);
    }

    // 세션을 제거하는 메서드
    public void removeSession(WebSocketSession session) {
        sessions.remove(session);
    }
}
