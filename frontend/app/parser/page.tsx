import AnalysisWorkspace from '@/components/AnalysisWorkspace';
export const metadata = { title: 'Dependency Parsing' };
export default function Page() {
  return <AnalysisWorkspace initialTask="parser" />;
}
