import { useEffect, useRef, useState, useCallback } from "react";
import { textToSpeech } from "../lib/elevenlabs";

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
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const [mode, setMode] = useState<"user" | "system">("user");
  const [toggleConversation, setToggleConversation] = useState<boolean>(false);

  const voiceId = "Atp5cNFg1Wj5gyKD7HWV";
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

  const stopRecording = useCallback(() => {
    const recorder = mediaRecorderRef.current;
    if (recorder && recorder.state !== "inactive") {
      recorder.stop();
    }
  }, []);

  const startUserRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      const recorder = new MediaRecorder(stream, {
        mimeType: "audio/webm",
      });
      recorder.ondataavailable = (event: BlobEvent) => {
        if (event.data.size > 0) {
          setAudioChunks((prev) => [...prev, event.data]);
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
            await textToSpeech({
              text: message,
              languageCode: language,
              voiceId,
            });

            if (answers) {
              stopRecording();
              ws.close();
              setStatus("closed");
            } else {
              await startUserRecording();
            }
          }
        } catch {
          const textResponse = event.data;
          await textToSpeech({
            text: textResponse,
            languageCode: language,
            voiceId,
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
  }, [wsUrl, userId, language, voiceId, startUserRecording, stopRecording]);

  const sendAudio = useCallback(() => {
    return new Promise<void>((resolve, reject) => {
      try {
        const recorder = mediaRecorderRef.current;
        const ws = wsRef.current;

        if (!recorder || !ws || ws.readyState !== WebSocket.OPEN) {
          reject(new Error("WebSocket is not connected"));
          return;
        }

        recorder.stop();

        recorder.onstop = async () => {
          const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
          const arrayBuffer = await audioBlob.arrayBuffer();
          const base64 = btoa(
            new Uint8Array(arrayBuffer).reduce(
              (data, byte) => data + String.fromCharCode(byte),
              ""
            )
          );

          ws.send(JSON.stringify({ audio: base64 }));
          setAudioChunks([]);
          setMode("system");
          resolve();
        };
      } catch (error) {
        reject(error);
      }
    });
  }, [audioChunks]);

  return {
    status,
    mode,
    toggleConversation,
    startRecording,
    sendAudio,
  };
}
