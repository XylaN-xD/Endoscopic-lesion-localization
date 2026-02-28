import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { 
  LayoutDashboard, Upload, BarChart3, Image, BookOpen, 
  GitBranch, MessageSquare, Lightbulb, ArrowLeft 
} from "lucide-react";
import OverviewSection from "@/components/workspace/OverviewSection";
import UploadSection from "@/components/workspace/UploadSection";
import DashboardSection from "@/components/workspace/DashboardSection";
import ImageExplorer from "@/components/workspace/ImageExplorer";
import GlossarySection from "@/components/workspace/GlossarySection";
import WorkflowSection from "@/components/workspace/WorkflowSection";
import ChatSection from "@/components/workspace/ChatSection";
import PromptsSection from "@/components/workspace/PromptsSection";
import ChatDrawer, { ChatDrawerTrigger } from "@/components/workspace/ChatDrawer";
import ThemeToggle from "@/components/ThemeToggle";

const tabs = [
  { id: "overview", label: "Overview", icon: LayoutDashboard },
  { id: "upload", label: "Dataset", icon: Upload },
  { id: "dashboard", label: "Analysis", icon: BarChart3 },
  { id: "viewer", label: "Image Explorer", icon: Image },
  { id: "glossary", label: "Glossary", icon: BookOpen },
  { id: "workflow", label: "Workflow", icon: GitBranch },
  { id: "chat", label: "Assistant", icon: MessageSquare },
  { id: "prompts", label: "Prompts", icon: Lightbulb },
];

const Workspace = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialTab = searchParams.get("tab") || "overview";
  const [activeTab, setActiveTab] = useState(initialTab);
  const [chatDrawerOpen, setChatDrawerOpen] = useState(false);

  const renderSection = () => {
    switch (activeTab) {
      case "overview": return <OverviewSection />;
      case "upload": return <UploadSection />;
      case "dashboard": return <DashboardSection />;
      case "viewer": return <ImageExplorer />;
      case "glossary": return <GlossarySection />;
      case "workflow": return <WorkflowSection />;
      case "chat": return <ChatSection />;
      case "prompts": return <PromptsSection />;
      default: return <OverviewSection />;
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Top navigation */}
      <header className="border-b border-border/50 bg-card/60 backdrop-blur-xl sticky top-0 z-50">
        <div className="flex items-center justify-between px-6 py-3">
          <div className="flex items-center gap-4">
            <button 
              onClick={() => navigate("/")}
              className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-all"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div className="w-px h-5 bg-border/50" />
            <div className="flex items-center gap-2.5">
              <div className="relative">
                <div className="w-2 h-2 rounded-full bg-primary" />
                <div className="absolute inset-0 w-2 h-2 rounded-full bg-primary/40 animate-ping" />
              </div>
              <span className="font-mono text-xs tracking-wider text-muted-foreground uppercase">
                ELL Workspace
              </span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <ThemeToggle />
            <span className="research-badge text-[10px]">
              <span className="w-1.5 h-1.5 rounded-full bg-current" />
              Phase 1
            </span>
          </div>
        </div>

        {/* Tab bar */}
        <div className="flex items-center gap-0.5 px-6 overflow-x-auto scrollbar-none">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`nav-tab flex items-center gap-2 whitespace-nowrap transition-all duration-300 ${
                  isActive ? "nav-tab-active" : ""
                }`}
              >
                <Icon className={`w-3.5 h-3.5 transition-colors duration-300 ${isActive ? "text-primary" : ""}`} />
                <span className="hidden sm:inline">{tab.label}</span>
              </button>
            );
          })}
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 p-6 pb-12">
        <div className="max-w-7xl mx-auto">
          {renderSection()}
        </div>
      </main>

      {/* Side drawer chat trigger & drawer */}
      {activeTab !== "chat" && (
        <ChatDrawerTrigger onClick={() => setChatDrawerOpen(true)} />
      )}
      <ChatDrawer isOpen={chatDrawerOpen} onClose={() => setChatDrawerOpen(false)} />
    </div>
  );
};

export default Workspace;
