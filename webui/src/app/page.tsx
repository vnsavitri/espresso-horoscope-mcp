'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import CardView from '@/components/CardView'
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
  const searchParams = useSearchParams()
  const mmdd = searchParams.get('mmdd')

  useEffect(() => {
    const fetchCards = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/cards.json')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        
        // If mmdd parameter is provided, filter the cards
        if (mmdd && mmdd.length === 4 && /^\d{4}$/.test(mmdd)) {
          const filteredReadings = filterCardsByBirthDate(data.readings, mmdd, 3)
          data.readings = filteredReadings
          data.metadata.total_shots = filteredReadings.length
          data.metadata.user_birth_mmdd = mmdd
        }
        
        setCards(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch cards')
      } finally {
        setLoading(false)
      }
    }

    fetchCards()
  }, [mmdd])

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading horoscope cards...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="text-destructive text-lg mb-2">Error</div>
          <p className="text-muted-foreground">{error}</p>
          <p className="text-sm text-muted-foreground mt-2">
            Make sure the backend server is running on http://127.0.0.1:8000
          </p>
        </div>
      </div>
    )
  }

  if (!cards || !cards.readings.length) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg mb-2">No Cards Found</div>
          <p className="text-muted-foreground">No horoscope cards available</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-4 max-w-4xl">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">☕ Espresso Horoscope</h1>
          <p className="text-muted-foreground text-sm">
            {cards.metadata.total_shots} reading{cards.metadata.total_shots !== 1 ? 's' : ''} • 
            User: {cards.metadata.user_birth_mmdd} • 
            Style: {cards.metadata.style_bank}
            {mmdd && (
              <span className="ml-2 px-2 py-1 bg-primary/10 text-primary text-xs rounded">
                Filtered for {mmdd}
              </span>
            )}
          </p>
        </div>

        <div className="space-y-4">
          {cards.readings.map((reading, index) => (
            <div key={reading.shot_id} className="w-full">
              <CardView reading={reading} />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}