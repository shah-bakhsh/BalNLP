import AnalysisWorkspace from '@/components/AnalysisWorkspace';
export const metadata = { title: 'Morphological Analysis' };
export default function Page() {
  return <AnalysisWorkspace initialTask="morph" />;
}
