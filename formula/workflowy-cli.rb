class WorkflowyCli < Formula
  desc "Command-line interface and MCP server for Workflowy"
  homepage "https://github.com/rodolfo-terriquez/workflowy-cli"
  version "3.3.5"
  url "https://github.com/rodolfo-terriquez/workflowy-cli/releases/download/v#{version}/wf-v#{version}-macos-arm64"
  sha256 "230d88acbfd4c91bc885cbb2b5cc9cede4b12f08384a4ddcbf7a80815e4559cc"

  depends_on arch: :arm64
  depends_on :macos

  def install
    bin.install "wf-v#{version}-macos-arm64" => "wf"
  end

  test do
    output = shell_output("#{bin}/wf --version 2>&1", 0)
    assert_match version.to_s, output
  end
end
