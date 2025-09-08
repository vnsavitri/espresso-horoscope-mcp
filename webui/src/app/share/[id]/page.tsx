'use client'

import { useEffect, useState } from 'react'
import { useParams, useSearchParams } from 'next/navigation'
import CardView from '@/components/CardView'

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

export default function SharePage() {
  const params = useParams()
  const searchParams = useSearchParams()
  const [card, setCard] = useState<Reading | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const cardId = params.id as string
  const format = searchParams.get('format')
  const isOG = format === 'og'

  useEffect(() => {
    const fetchCard = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/cards.json')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data: CardsResponse = await response.json()
        
        const cardIndex = parseInt(cardId)
        if (isNaN(cardIndex) || cardIndex < 0 || cardIndex >= data.readings.length) {
          throw new Error(`Invalid card index: ${cardId}`)
        }
        
        setCard(data.readings[cardIndex])
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch card')
      } finally {
        setLoading(false)
      }
    }

    fetchCard()
  }, [cardId])

  if (loading) {
    return (
      <div className={`${isOG ? 'w-[1200px] h-[630px]' : 'w-[1080px] h-[1350px]'} bg-background flex items-center justify-center`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading card...</p>
        </div>
      </div>
    )
  }

  if (error || !card) {
    return (
      <div className={`${isOG ? 'w-[1200px] h-[630px]' : 'w-[1080px] h-[1350px]'} bg-background flex items-center justify-center`}>
        <div className="text-center">
          <div className="text-destructive text-lg mb-2">Error</div>
          <p className="text-muted-foreground">{error || 'Card not found'}</p>
        </div>
      </div>
    )
  }

  return <CardView reading={card} isOG={isOG} />
}
