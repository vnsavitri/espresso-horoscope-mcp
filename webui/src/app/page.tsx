'use client'

import { useEffect, useState } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { filterCardsByBirthDate } from '@/lib/picker'

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

interface CardsResponse {
  metadata: {
    generated_at: string
    user_birth_mmdd: string
    style_bank: string
    total_shots: number
  }
  readings: Reading[]
}

export default function Home() {
  const [cards, setCards] = useState<CardsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [birthDate, setBirthDate] = useState('')
  const [showInput, setShowInput] = useState(true)
  const [initialized, setInitialized] = useState(false)
  const searchParams = useSearchParams()
  const router = useRouter()
  const mmdd = searchParams.get('mmdd')

  useEffect(() => {
    if (!initialized) {
      // Check URL parameters on client side
      const urlParams = new URLSearchParams(window.location.search)
      const urlMmdd = urlParams.get('mmdd')
      
      if (urlMmdd) {
        setBirthDate(urlMmdd)
        setShowInput(false)
        fetchCards(urlMmdd)
      } else {
        setLoading(false)
      }
      setInitialized(true)
    }
  }, [initialized])

  const fetchCards = async (mmddParam: string) => {
    setLoading(true)
    try {
      // Generate new cards for this specific birth date
      const response = await fetch(`http://127.0.0.1:8000/generate_cards?mmdd=${mmddParam}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      setCards(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate cards')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (birthDate.length === 4 && /^\d{4}$/.test(birthDate)) {
      // Generate new cards for this date
      fetchCards(birthDate)
      setShowInput(false)
    }
  }


  if (showInput) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
        <div className="max-w-md w-full">
          <Card className="bg-white/10 backdrop-blur-md border-white/20">
            <CardHeader className="text-center">
              <CardTitle className="text-3xl font-bold text-white mb-2">
                ☕ Espresso Horoscope
              </CardTitle>
              <p className="text-white/80">
                Discover your cosmic coffee destiny
              </p>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="birthDate" className="block text-sm font-medium text-white mb-2">
                    Enter your birth date (MMDD)
                  </label>
                  <input
                    type="text"
                    id="birthDate"
                    value={birthDate}
                    onChange={(e) => setBirthDate(e.target.value)}
                    placeholder="e.g., 1021 for October 21st"
                    maxLength={4}
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent"
                  />
                  <p className="text-xs text-white/60 mt-1">
                    Format: MMDD (e.g., 1021 for October 21st)
                  </p>
                </div>
                <button
                  type="submit"
                  disabled={birthDate.length !== 4 || !/^\d{4}$/.test(birthDate)}
                  className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 rounded-lg font-semibold hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  Generate my espresso horoscope
                </button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white/80 text-lg">Reading the cosmic coffee grounds...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <Card className="max-w-md w-full bg-white/10 backdrop-blur-md border-white/20">
          <CardContent className="p-6 text-center">
            <div className="text-red-400 text-lg mb-2">Error</div>
            <p className="text-white/80 mb-4">{error}</p>
            <p className="text-sm text-white/60">
              Make sure the backend server is running on http://127.0.0.1:8000
            </p>
            <button
              onClick={() => {
                setShowInput(true)
                setCards(null)
                setError(null)
              }}
              className="mt-4 bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30 transition-colors"
            >
              Try Again
            </button>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!cards || !cards.readings.length) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <Card className="max-w-md w-full bg-white/10 backdrop-blur-md border-white/20">
          <CardContent className="p-6 text-center">
            <div className="text-white text-lg mb-2">No Cards Found</div>
            <p className="text-white/80 mb-4">No horoscope cards available</p>
            <button
              onClick={() => {
                setShowInput(true)
                setCards(null)
                setError(null)
              }}
              className="bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30 transition-colors"
            >
              Try Different Date
            </button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-white mb-2">☕ Espresso Horoscope</h1>
          <p className="text-white/80 text-lg">
            Your cosmic coffee destiny for {cards.metadata.user_birth_mmdd}
          </p>
          <button
            onClick={() => {
              setShowInput(true)
              setCards(null)
              setError(null)
            }}
            className="mt-4 bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30 transition-colors"
          >
            Try Different Date
          </button>
        </div>

        <div className="space-y-8">
          {cards.readings.map((reading, index) => (
            <Card key={reading.shot_id} className="bg-white/10 backdrop-blur-md border-white/20 overflow-hidden">
              <CardContent className="p-0">
                {/* Card Header with Zodiac */}
                <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-6 text-center">
                  <div className="text-4xl mb-2">{reading.card.zodiac_icon}</div>
                  <h2 className="text-2xl font-bold text-white mb-1">{reading.card.title}</h2>
                  <p className="text-white/90 italic">"{reading.card.mantra}"</p>
                </div>

                {/* Metrics Row */}
                <div className="p-6 bg-white/5">
                  <div className="grid grid-cols-5 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-white">{reading.card.snapshot.brew_ratio.toFixed(2)}:1</div>
                      <div className="text-xs text-white/60">Ratio</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-white">{reading.card.snapshot.shot_time.toFixed(0)}s</div>
                      <div className="text-xs text-white/60">Time</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-white">{reading.card.snapshot.peak_pressure.toFixed(1)} bar</div>
                      <div className="text-xs text-white/60">Pressure</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-white">{reading.card.snapshot.temp_avg.toFixed(1)}°C</div>
                      <div className="text-xs text-white/60">Temp</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-white">{reading.card.snapshot.channeling.toFixed(2)}</div>
                      <div className="text-xs text-white/60">Channel</div>
                    </div>
                  </div>
                </div>

                {/* Advice */}
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-white mb-3">Cosmic Guidance</h3>
                  <ul className="space-y-2">
                    {reading.card.advice.slice(0, 3).map((advice, i) => (
                      <li key={i} className="text-white/80 flex items-start">
                        <span className="text-purple-400 mr-2">•</span>
                        {advice}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Narrative */}
                <div className="p-6 bg-white/5">
                  <p className="text-white/90 leading-relaxed">
                    {reading.card.template.split('\n').slice(0, 2).join(' ')}
                  </p>
                </div>

                {/* Meta */}
                <div className="p-6 bg-white/5 border-t border-white/10">
                  <div className="text-center">
                    <div className="text-xs text-white/60">
                      {reading.card.zodiac_icon} {reading.card.zodiac} • {reading.user_context.style_preference}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}