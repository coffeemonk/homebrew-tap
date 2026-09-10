class WorkflowyCli < Formula
  desc "Command-line interface and MCP server for Workflowy"
  homepage "https://github.com/rodolfo-terriquez/workflowy-cli"
  version "3.3.5"

  on_macos do
    on_arm do
      url "https://github.com/rodolfo-terriquez/workflowy-cli/releases/download/v#{version}/wf-v#{version}-macos-arm64"
      sha256 "230d88acbfd4c91bc885cbb2b5cc9cede4b12f08384a4ddcbf7a80815e4559cc"
    end
    on_intel do
      url "https://github.com/rodolfo-terriquez/workflowy-cli/releases/download/v#{version}/wf-v#{version}-macos-x64"
      sha256 "4932af3b4e395dd8778b2130b15dc052687142d7cf829722b53a5f917d58b7ee"
    end
  end

  def install
    binary_name = Hardware::CPU.arm? ? "wf-v#{version}-macos-arm64" : "wf-v#{version}-macos-x64"
    bin.install binary_name => "wf"
  end

  test do
    output = shell_output("#{bin}/wf --version 2>&1", 0)
    assert_match version.to_s, output
  end
end
