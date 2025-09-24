interface Voice {
  text: string;
  languageCode: string;
  voiceName?: string;
  onEnd?: () => void;
}

export const speak = ({ text, languageCode, voiceName, onEnd }: Voice) => {
  const synth = window.speechSynthesis;
  let voices = synth.getVoices();

  const createUtterance = () => {
    const utterance = new SpeechSynthesisUtterance(text);
    if (voiceName) {
      const selected = voices.find((voice) => voice.name === voiceName);
      if (selected) {
        utterance.voice = selected;
      }
    } else if (languageCode) {
      const selected = voices.find((voice) => voice.lang === languageCode);
      if (selected) {
        utterance.voice = selected;
      }
    }
    if (onEnd) {
      utterance.onend = onEnd;
    }
    synth.speak(utterance);
  };
  if (!voices.length) {
    synth.onvoiceschanged = () => {
      voices = synth.getVoices();
      createUtterance();
    };
  } else {
    createUtterance();
  }
};
