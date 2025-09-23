interface AudioAnimationsProps {
	mode: "user" | "system"
}

export default function AudioAnimations({ mode = "system" }: AudioAnimationsProps) {
	return (
		<div className="flex flex-col justify-center items-center gap-4 mt-8">
			{
				mode === "system" && (
					<>
						<div className="flex flex-row justify-center items-center gap-1">
							<div className="w-1 h-1 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-2 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-3 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-4 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-5 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-7 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-5 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-4 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-3 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-2 bg-black animate-pulse rounded-4xl" />
							<div className="w-1 h-1 bg-black animate-pulse rounded-4xl" />
						</div>
						<span className="font-poppins text-sm text-gray-800 animate-pulse">
							I'm speaking...
						</span>
					</>
				)
			}
			{
				mode === "user" && (
					<>
						<svg xmlns="http://www.w3.org/2000/svg" className="animate-pulse" width="30" height="30" viewBox="0 0 48 48"><g fill="none" stroke="#000000" stroke-linejoin="round" stroke-width="4"><rect width="14" height="27" x="17" y="4" fill="#000000" rx="7"/><path stroke-linecap="round" d="M9 23c0 8.284 6.716 15 15 15s15-6.716 15-15M24 38v6"/></g></svg>
						<span className="font-poppins text-sm text-gray-800 animate-pulse">
							I'm listening...
						</span>
					</>
				)
			}
		</div>
	)
}