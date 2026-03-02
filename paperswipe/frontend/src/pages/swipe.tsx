import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { apiGet, apiPost } from '../lib/api';
import SwipeDeck from '../components/SwipeDeck';
import JobProgress from '../components/JobProgress';

export default function SwipePage() {
  const router = useRouter();
  const { job, query } = router.query;
  const [papers, setPapers] = useState<any[]>([]);
  useEffect(() => {
    if (!query) return;
    apiGet(`/api/papers/queue?publication=TIFS&query=${encodeURIComponent(String(query))}&only_unswiped=1&limit=30`).then(setPapers);
  }, [query]);

  return <main style={{padding:20}}>
    <h2>Swipe</h2>
    {job && <JobProgress jobId={String(job)} />}
    <SwipeDeck papers={papers} onLike={async (id,tags)=>{await apiPost('/api/swipe',{paper_id:id,decision:'LIKED',tags});}} onSkip={async (id)=>{await apiPost('/api/swipe',{paper_id:id,decision:'SKIPPED',tags:[]});}} />
  </main>
}
