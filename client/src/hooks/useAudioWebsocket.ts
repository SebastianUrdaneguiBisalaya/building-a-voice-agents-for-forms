import { useEffect, useRef, useState, useCallback } from "react";
import { speak } from "../lib/voice";

type UseAudioWebsocketOptions = {
  wsUrl: string;
  userId: string;
  language: string;
};

type WebSocketStatus = "idle" | "connecting" | "connected" | "error" | "closed";

export function useAudioWebSocket({
  wsUrl,
  userId,
  language,
}: UseAudioWebsocketOptions) {
  const [status, setStatus] = useState<WebSocketStatus>("idle");
  const [mode, setMode] = useState<"user" | "system">("system");
  const [toggleConversation, setToggleConversation] = useState<boolean>(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    async function requestPermission() {
      try {
        await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
      } catch (error) {
        console.error("Error requesting audio permission:", error);
      }
    }
    requestPermission();
  }, []);

  const startUserRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      const recorder = new MediaRecorder(stream, {
        mimeType: "audio/webm",
      });

      const chunks: Blob[] = [];

      recorder.ondataavailable = (event: BlobEvent) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      recorder.onstop = async () => {
        try {
          const ws = wsRef.current;
          if (!ws || ws.readyState !== WebSocket.OPEN) return;

          const audioBlob = new Blob(chunks, { type: "audio/webm" });
          const arrayBuffer = await audioBlob.arrayBuffer();
          const base64 = btoa(
            new Uint8Array(arrayBuffer).reduce(
              (data, byte) => data + String.fromCharCode(byte),
              ""
            )
          );
          ws.send(JSON.stringify({ audio: base64 }));
          setMode("system");
        } catch (error) {
          console.error("Error sending audio:", error);
        }
      };
      recorder.start();
      mediaRecorderRef.current = recorder;
      setMode("user");
    } catch (error) {
      console.error("Error starting user recording:", error);
    }
  }, []);

  const startRecording = useCallback(async () => {
    setToggleConversation((prev) => !prev);
    try {
      const url = `${wsUrl}?user_id=${encodeURIComponent(
        userId
      )}&language=${encodeURIComponent(language)}`;
      const ws = new WebSocket(url);

      ws.onopen = () => setStatus("connected");

      ws.onerror = () => {
        setStatus("error");
        setToggleConversation((prev) => !prev);
      };

      ws.onclose = () => {
        setStatus("closed");
        setToggleConversation((prev) => !prev);
      };

      ws.onmessage = async (event: MessageEvent) => {
        try {
          const data = JSON.parse(event.data);
          const { message, answers } = data;
          if (message) {
            speak({
              text: message,
              languageCode: language,
              voiceName: "Google UK English Male",
            });

            if (answers) {
              ws.close();
              setStatus("closed");
            } else {
              await startUserRecording();
            }
          }
        } catch {
          const textResponse = event.data;
          speak({
            text: textResponse,
            languageCode: language,
            voiceName: "Google UK English Male",
          });
          await startUserRecording();
        }
      };

      wsRef.current = ws;
      setStatus("connecting");
    } catch (error) {
      console.error("Error starting recording:", error);
      setStatus("error");
    }
  }, [wsUrl, userId, language, startUserRecording]);

  const sendAudio = useCallback(() => {
    const recorder = mediaRecorderRef.current;
    if (recorder && recorder.state !== "inactive") {
      recorder.stop();
    }
  }, []);

  return {
    status,
    mode,
    toggleConversation,
    startRecording,
    sendAudio,
  };
}
