import { JSX } from 'react';

type Entity = {
  entity: string
  label: string
  start_idx: number
  end_idx: number
}

interface HighlightedTextProps {
  body: string;
  entities: Entity[];
}

const HighlightedText = ({ body, entities }: HighlightedTextProps) => {
  const labelColors: { [key: string]: string } = {
    CARDINAL: 'bg-pink-100',       // Numbers
    DATE: 'bg-purple-100',         // Dates
    EVENT: 'bg-red-100',           // Events
    FAC: 'bg-indigo-100',          // Facilities
    GPE: 'bg-blue-100',            // Geo-political entities
    LANGUAGE: 'bg-amber-100',      // Languages
    LAW: 'bg-rose-100',            // Legal documents
    LOC: 'bg-cyan-100',            // Locations
    MONEY: 'bg-yellow-100',        // Monetary values
    NORP: 'bg-lime-100',           // Nationalities/religious/political groups
    ORDINAL: 'bg-fuchsia-100',     // Ordinal numbers
    ORG: 'bg-orange-100',          // Organizations
    PERCENT: 'bg-teal-100',        // Percentages
    PERSON: 'bg-green-100',        // People
    PRODUCT: 'bg-emerald-100',     // Products
    QUANTITY: 'bg-violet-100',     // Quantities
    TIME: 'bg-sky-100',            // Times
    WORK_OF_ART: 'bg-pink-100',    // Creative works
  };

  // Create an array of text fragments and entities
  const fragments = entities
    .sort((a, b) => a.start_idx - b.start_idx)
    .reduce<Array<{ text: string; entity?: Entity }>>((acc, entity) => {
      const lastEnd = acc.length > 0 ? acc[acc.length - 1].entity?.end_idx || 0 : 0;

      // Add preceding text if there's a gap
      if (entity.start_idx > lastEnd) {
        acc.push({
          text: body.slice(lastEnd, entity.start_idx)
        });
      }

      // Add the entity
      acc.push({
        text: body.slice(entity.start_idx, entity.end_idx),
        entity
      });

      return acc;
    }, []);

  // Add remaining text after last entity
  const lastEntityEnd = entities[entities.length - 1]?.end_idx || 0;
  if (lastEntityEnd < body.length) {
    fragments.push({
      text: body.slice(lastEntityEnd)
    });
  }

  return (
    <div className="whitespace-pre-wrap bg-gray-50 p-4 rounded-lg border border-gray-200">
      {fragments.map((fragment, index) => {
        if (fragment.entity) {
          return (
            <span
              key={`entity-${index}`}
              className={`px-1.5 py-0.5 rounded-sm text-sm font-medium ${labelColors[fragment.entity.label] || 'bg-gray-100'
                } hover:ring-1 hover:ring-current`}
              title={fragment.entity.label}
            >
              {fragment.text}
            </span>
          );
        }
        return <span key={`text-${index}`}>{fragment.text}</span>;
      })}
    </div>
  );
};

export default HighlightedText;