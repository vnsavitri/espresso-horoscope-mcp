'use client'

import { Badge } from '@/components/ui/badge'

interface Snapshot {
  brew_ratio: number
  shot_time: number
  peak_pressure: number
  temp_avg: number
  channeling: number
}

interface CardData {
  emoji: string
  title: string
  mantra: string
  rule_hit: string
  seed: string
  zodiac: string
  zodiac_icon: string
  snapshot: Snapshot
  advice: string[]
  flavour_line: string
  template: string
}

interface Reading {
  shot_id: string
  user_context: {
    birth_mmdd: string
    style_preference: string
    generation_date: string
  }
  card: CardData
}

interface CardViewProps {
  reading: Reading
  isOG?: boolean
}

// Zodiac color mapping
const zodiacColors: Record<string, string> = {
  'Aries': 'text-red-500',
  'Taurus': 'text-green-500', 
  'Gemini': 'text-yellow-500',
  'Cancer': 'text-blue-500',
  'Leo': 'text-orange-500',
  'Virgo': 'text-emerald-500',
  'Libra': 'text-pink-500',
  'Scorpio': 'text-purple-500',
  'Sagittarius': 'text-indigo-500',
  'Capricorn': 'text-gray-600',
  'Aquarius': 'text-cyan-500',
  'Pisces': 'text-teal-500'
}

export default function CardView({ reading, isOG = false }: CardViewProps) {
  const { card } = reading
  const zodiacColor = zodiacColors[card.zodiac] || 'text-gray-500'
  
  return (
    <div className={`${isOG ? 'w-[1200px] h-[630px]' : 'w-[768px] h-[1024px]'} bg-gradient-to-b from-neutral-50 to-neutral-100 flex flex-col justify-between p-8`}>
      {/* Main Content */}
      <div className="flex-1 flex flex-col justify-center">
        {/* Zodiac Icon and Title */}
        <div className="text-center mb-4">
          <div className={`${isOG ? 'text-4xl' : 'text-4xl'} mb-3 ${zodiacColor}`}>
            {card.zodiac_icon}
          </div>
          <h1 className={`${isOG ? 'text-2xl' : 'text-2xl'} font-bold mb-2 text-neutral-800`}>
            {card.title}
          </h1>
          <p className="text-sm text-neutral-600 italic">
            "{card.mantra}"
          </p>
        </div>

        {/* Snapshot Badges */}
        <div className="flex justify-center mb-4">
          <div className="flex flex-wrap gap-2 justify-center">
            <Badge variant="secondary" className="text-xs font-mono">
              <span className="font-bold">{card.snapshot.brew_ratio.toFixed(2)}</span>:1
            </Badge>
            <Badge variant="secondary" className="text-xs font-mono">
              <span className="font-bold">{card.snapshot.shot_time}</span>s
            </Badge>
            <Badge variant="secondary" className="text-xs font-mono">
              <span className="font-bold">{card.snapshot.peak_pressure.toFixed(1)}</span> bar
            </Badge>
            <Badge variant="secondary" className="text-xs font-mono">
              <span className="font-bold">{card.snapshot.temp_avg.toFixed(1)}</span>°C
            </Badge>
            <Badge variant="secondary" className="text-xs font-mono">
              <span className="font-bold">{card.snapshot.channeling.toFixed(2)}</span>
            </Badge>
          </div>
        </div>

        {/* Advice List */}
        <div className="text-center mb-4">
          <ul className="space-y-1 max-w-md mx-auto">
            {card.advice.slice(0, 3).map((advice, index) => (
              <li key={index} className="text-sm text-neutral-600">
                • {advice}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Footer */}
      <div className="text-center space-y-2">
        <p className="text-xs text-neutral-500">
          {card.flavour_line}
        </p>
        {/* Meta Information */}
        <div className="text-xs text-neutral-400 space-x-3">
          <span>seed: {card.seed.slice(0, 8)}</span>
          <span>•</span>
          <span>rule: {card.rule_hit}</span>
          <span>•</span>
          <span>severity: {card.rule_hit === 'sweet_spot' ? 'perfect' : 'warning'}</span>
        </div>
        {/* Constellation and Tones */}
        <div className="text-xs text-neutral-400">
          {card.zodiac_icon} {card.zodiac} • {reading.user_context.style_preference}
        </div>
      </div>
    </div>
  )
}
