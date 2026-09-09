import AnalysisWorkspace from '@/components/AnalysisWorkspace';
export const metadata = { title: 'POS Tagging' };
export default function Page() {
  return <AnalysisWorkspace initialTask="pos" />;
}
