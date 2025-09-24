interface AnswersProps {
	answers: Record<string, string | number | boolean>
}

export default function Answers({ answers }: AnswersProps) {
	return (
		<div className="p-4 max-w-4xl w-full grow flex flex-col gap-6 overflow-y-auto">
			<h2 className="font-bold font-bricolage-grotesque text-lg">Questions and Answers (Q&A)</h2>
			<div className="flex flex-col">
				{
					Object.entries(answers).map(([key, value]) => (
						<div
							key={key}
							className="p-4 border-t border-orange-200 flex flex-col gap-2"
						>
							<span className="font-bricolage-grotesque font-semibold text-sm">{key}</span>
							<p className="font-poppins">{value}</p>
						</div>
					))
				}
			</div>
		</div>
	)
}