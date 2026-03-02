import { useState } from 'react';
import PaperCard from './PaperCard';
import { Paper } from '../lib/types';

export default function SwipeDeck({ papers, onLike, onSkip }: { papers: Paper[]; onLike: (id: string, tags: string[]) => void; onSkip: (id: string) => void }) {
  const [idx, setIdx] = useState(0);
  const paper = papers[idx];
  if (!paper) return <div>No more papers</div>;
  return <PaperCard paper={paper} onLike={(tags) => { onLike(paper.id, tags); setIdx(idx + 1); }} onSkip={() => { onSkip(paper.id); setIdx(idx + 1); }} />;
}
