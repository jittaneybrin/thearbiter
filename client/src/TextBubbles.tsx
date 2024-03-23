import { Session, Chatbox } from "@talkjs/react";

export default function Chat() {
  return (
    <Session appId="t4KsGHvY" userId="sample_user_alice">
      <Chatbox
        conversationId="sample_conversation"
        style={{ width: "100%", height: "500px" }}
      />
    </Session>
  );
}
