import { Paper } from '../lib/types';

export default function PaperCard({ paper, onLike, onSkip }: { paper: Paper; onLike: (tags: string[]) => void; onSkip: () => void }) {
  return (
    <div style={{border:'1px solid #ddd', padding:16, borderRadius:8, maxWidth:800}}>
      <h3>{paper.title}</h3>
      <p>{paper.year} | {paper.authors?.join(', ')}</p>
      <p>{paper.summary?.one_liner || 'Summarizing...'}</p>
      <details><summary>Abstract</summary><p>{paper.abstract || 'N/A'}</p></details>
      <p><a href={paper.xplore_url} target="_blank">Open Xplore</a></p>
      <button onClick={() => onLike(['FL'])}>Like (Left)</button>
      <button onClick={onSkip} style={{marginLeft:8}}>Skip (Right)</button>
    </div>
  );
}
