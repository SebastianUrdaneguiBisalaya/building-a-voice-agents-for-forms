import { ElevenLabsClient, play } from "@elevenlabs/elevenlabs-js";

interface ElevenLabsConfig {
  text: string;
  languageCode: string;
  voiceId: string;
}

const elevenlabs = new ElevenLabsClient({
  apiKey: import.meta.env.ELEVEN_LABS_KEY,
});

function readableStreamToAsyncIterable<T>(
  stream: ReadableStream<T>
): AsyncIterable<T> {
  const reader = stream.getReader();
  return {
    [Symbol.asyncIterator](): AsyncIterator<T> {
      return {
        async next(): Promise<IteratorResult<T>> {
          const { done, value } = await reader.read();
          if (done) {
            return { done: true, value: undefined };
          }
          return { done: false, value: value as T };
        },
      };
    },
  };
}

export const textToSpeech = async ({
  text,
  languageCode,
  voiceId,
}: ElevenLabsConfig) => {
  const audioStream = await elevenlabs.textToSpeech.convert(voiceId, {
    text: text,
    modelId: "eleven_multilingual_v2",
    outputFormat: "mp3_44100_128",
    languageCode: languageCode,
  });
  const iterable = readableStreamToAsyncIterable(audioStream);
  return await play(iterable);
};
