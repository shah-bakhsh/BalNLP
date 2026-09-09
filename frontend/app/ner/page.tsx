import AnalysisWorkspace from '@/components/AnalysisWorkspace';
export const metadata = { title: 'Named Entity Recognition' };
export default function Page() {
  return <AnalysisWorkspace initialTask="ner" />;
}
