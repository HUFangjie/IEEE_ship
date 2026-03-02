export type Paper = {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  doi?: string;
  year: number;
  xplore_url: string;
  is_oa: number;
  summary?: any;
  summary_md?: string;
};
