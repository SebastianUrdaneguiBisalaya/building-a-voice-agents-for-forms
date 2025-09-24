import './App.css'
import AudioAnimations from './components/audio-animations'
import { useAudioWebSocket } from './hooks/useAudioWebsocket'

function App() {
	const { mode, sendAudio, toggleConversation, startRecording } = useAudioWebSocket({
		wsUrl: "ws://localhost:8000/api/v1/ws/voice-agents",
		userId: "user-1",
		languageToClient: "en-GB",
		languageToServer: "en",
	});


  return (
    <div className='w-full h-screen flex flex-col justify-center items-center bg-[#FFEFBA] bg-gradient-to-t from-[#FFEFBA] to-[#FFFFFF]'>
			<main className='w-full max-w-6xl h-full flex flex-col justify-center items-center gap-4'>
				<h1 className='font-bricolage-grotesque text-5xl font-bold text-center'>Voice Agent for Forms</h1>
				<p className='font-poppins text-sm text-gray-600'>I recommend checking that the audio is enabled in your laptop.</p>
				{
					!toggleConversation && (
						<button
							className='p-4 bg-orange-300 rounded-2xl hover:bg-amber-500 cursor-pointer font-bricolage-grotesque mt-8'
							onClick={startRecording}
						>
							I'm ready to start
						</button>
					)
				}
				{
					toggleConversation && (
						<AudioAnimations mode={mode} />
					)
				}
				{
					toggleConversation && mode === "user" && (
						<button
							className='p-4 bg-orange-300 rounded-2xl hover:bg-amber-500 cursor-pointer font-bricolage-grotesque mt-8'
							onClick={sendAudio}
						>
							Send answer
						</button>
					)
				}
			</main>
			<footer className='p-4'>
				<span className='font-poppins text-sm text-gray-600'>Made with 🧡 by <a className='font-medium cursor-pointer underline' href="https://sebastianurdanegui.com" target='_blank'>Sebastian Marat Urdanegui Bisalaya</a></span>
			</footer>
		</div>
  )
}

export default App
