package com.example.websocket_demo.handler;

import org.springframework.web.socket.handler.TextWebSocketHandler;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import java.io.IOException;

public class CrawlerWebSocketHandler extends TextWebSocketHandler {


    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) throws IOException {
        // 클라이언트에서 메시지를 받으면 처리하는 메서드
        System.out.println("클라이언트로부터 메시지 수신: " + message.getPayload());
    }

    public void sendCrawledData(WebSocketSession session, String data) throws IOException {
        // 크롤링된 데이터를 클라이언트에 전송
        TextMessage textMessage = new TextMessage(data);
        session.sendMessage(textMessage);
    }


}
