"use client"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { motion } from "framer-motion"

type Entity = {
  entity: string
  label: string
  start_idx: number
  end_idx: number
}

interface HighlightedTextProps {
  body: string
  entities: Entity[]
}

const HighlightedText = ({ body, entities }: HighlightedTextProps) => {
  // More refined color palette with opacity for a subtle look
  const labelColors: { [key: string]: { bg: string; border: string; text: string } } = {
    CARDINAL: { bg: "bg-primary/5", border: "border-primary/20", text: "text-primary-foreground" },
    DATE: { bg: "bg-violet-500/5", border: "border-violet-500/20", text: "text-violet-700" },
    EVENT: { bg: "bg-red-500/5", border: "border-red-500/20", text: "text-red-700" },
    FAC: { bg: "bg-indigo-500/5", border: "border-indigo-500/20", text: "text-indigo-700" },
    GPE: { bg: "bg-blue-500/5", border: "border-blue-500/20", text: "text-blue-700" },
    LANGUAGE: { bg: "bg-amber-500/5", border: "border-amber-500/20", text: "text-amber-700" },
    LAW: { bg: "bg-rose-500/5", border: "border-rose-500/20", text: "text-rose-700" },
    LOC: { bg: "bg-cyan-500/5", border: "border-cyan-500/20", text: "text-cyan-700" },
    MONEY: { bg: "bg-yellow-500/5", border: "border-yellow-500/20", text: "text-yellow-700" },
    NORP: { bg: "bg-lime-500/5", border: "border-lime-500/20", text: "text-lime-700" },
    ORDINAL: { bg: "bg-fuchsia-500/5", border: "border-fuchsia-500/20", text: "text-fuchsia-700" },
    ORG: { bg: "bg-orange-500/5", border: "border-orange-500/20", text: "text-orange-700" },
    PERCENT: { bg: "bg-teal-500/5", border: "border-teal-500/20", text: "text-teal-700" },
    PERSON: { bg: "bg-green-500/5", border: "border-green-500/20", text: "text-green-700" },
    PRODUCT: { bg: "bg-emerald-500/5", border: "border-emerald-500/20", text: "text-emerald-700" },
    QUANTITY: { bg: "bg-violet-500/5", border: "border-violet-500/20", text: "text-violet-700" },
    TIME: { bg: "bg-sky-500/5", border: "border-sky-500/20", text: "text-sky-700" },
    WORK_OF_ART: { bg: "bg-pink-500/5", border: "border-pink-500/20", text: "text-pink-700" },
  }

  // Create an array of text fragments and entities
  const fragments = entities
    .sort((a, b) => a.start_idx - b.start_idx)
    .reduce<Array<{ text: string; entity?: Entity }>>((acc, entity) => {
      const lastEnd = acc.length > 0 ? acc[acc.length - 1].entity?.end_idx || 0 : 0

      // Add preceding text if there's a gap
      if (entity.start_idx > lastEnd) {
        acc.push({
          text: body.slice(lastEnd, entity.start_idx),
        })
      }

      // Add the entity
      acc.push({
        text: body.slice(entity.start_idx, entity.end_idx),
        entity,
      })

      return acc
    }, [])

  // Add remaining text after last entity
  const lastEntityEnd =
    fragments.length > 0 && fragments[fragments.length - 1].entity ? fragments[fragments.length - 1].entity!.end_idx : 0

  if (lastEntityEnd < body.length) {
    fragments.push({
      text: body.slice(lastEntityEnd),
    })
  }

  // If there are no entities or fragments, just return the body
  if (fragments.length === 0) {
    return <div className="whitespace-pre-wrap leading-relaxed">{body}</div>
  }

  return (
    <TooltipProvider delayDuration={300}>
      <div className="whitespace-pre-wrap leading-relaxed p-5 rounded-lg bg-card text-card-foreground">
        {fragments.map((fragment, index) => {
          if (fragment.entity) {
            const colorSet = labelColors[fragment.entity.label] || {
              bg: "bg-gray-100",
              border: "border-gray-200",
              text: "text-gray-700",
            }

            return (
              <Tooltip key={`entity-${index}`}>
                <TooltipTrigger asChild>
                  <motion.span
                    initial={{ opacity: 0.8 }}
                    animate={{ opacity: 1 }}
                    whileHover={{
                      scale: 1.1, // Increased zoom effect
                      transition: { duration: 0.2 },
                    }}
                    className={`inline-block px-1.5 py-0.5 rounded border ${colorSet.bg} ${colorSet.border} ${colorSet.text} 
                      text-sm font-medium cursor-help transition-all duration-200 ease-in-out`}
                  >
                    {fragment.text}
                  </motion.span>
                </TooltipTrigger>
                <TooltipContent side="top" className="font-medium">
                  <div className="flex flex-col">
                    <span className="text-xs uppercase tracking-wide text-muted-foreground">
                      {fragment.entity.label}
                    </span>
                    <span className="text-sm">{fragment.entity.entity}</span>
                  </div>
                </TooltipContent>
              </Tooltip>
            )
          }
          return (
            <span key={`text-${index}`} className="text-foreground">
              {fragment.text}
            </span>
          )
        })}
      </div>
    </TooltipProvider>
  )
}

export default HighlightedText

