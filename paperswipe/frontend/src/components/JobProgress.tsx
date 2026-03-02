import { useEffect, useState } from 'react';
import { apiGet } from '../lib/api';

export default function JobProgress({ jobId }: { jobId: string }) {
  const [job, setJob] = useState<any>();
  useEffect(() => {
    if (!jobId) return;
    const t = setInterval(async () => setJob(await apiGet(`/api/jobs/${jobId}`)), 1000);
    return () => clearInterval(t);
  }, [jobId]);
  if (!job) return null;
  const pct = job.total ? Math.floor((job.done / job.total) * 100) : 0;
  return <div>Job: {job.status} {job.done}/{job.total} ({pct}%) {job.error && `Error: ${job.error}`}</div>;
}
