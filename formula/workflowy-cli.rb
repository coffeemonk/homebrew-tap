class WorkflowyCli < Formula
  desc "Command-line interface and MCP server for Workflowy"
  homepage "https://github.com/rodolfo-terriquez/workflowy-cli"
  version "3.3.2"

  on_macos do
    on_arm do
      url "https://github.com/rodolfo-terriquez/workflowy-cli/releases/download/v#{version}/workflowy-cli_#{version}_darwin_arm64.tar.gz"
      sha256 "0019dfc4b32d63c1392aa264aed2253c1e0c2fb09216f8e2cc269bbfb8bb49b5"
    end
    on_intel do
      url "https://github.com/rodolfo-terriquez/workflowy-cli/releases/download/v#{version}/workflowy-cli_#{version}_darwin_amd64.tar.gz"
      sha256 "0019dfc4b32d63c1392aa264aed2253c1e0c2fb09216f8e2cc269bbfb8bb49b5"
    end
  end

  def install
    if File.exist?("workflowy-cli")
      bin.install "workflowy-cli" => "wf"
    elsif File.exist?("wf")
      bin.install "wf"
    end
  end

  test do
    output = shell_output("#{bin}/wf --version 2>&1", 0)
    assert_match "workflowy-cli", output.downcase
  end
end
