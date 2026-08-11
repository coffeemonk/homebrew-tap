class WorkflowyCli < Formula
  desc "Command-line interface and MCP server for Workflowy"
  homepage "https://github.com/rodolfo-terriquez/workflowy-cli"
  version "3.3.3"

  on_macos do
    on_arm do
      url "https://github.com/rodolfo-terriquez/workflowy-cli/releases/download/v#{version}/wf-v#{version}-macos-arm64"
      sha256 "16a853c03bed909701c32d9719a1e82b15b454aa954e953052e4344dd3ae98f1"
    end
    on_intel do
      url "https://github.com/rodolfo-terriquez/workflowy-cli/releases/download/v#{version}/wf-v#{version}-macos-x64"
      sha256 "1bd45f905d913d120c843f8e9e2cc84e66acf9895718bae07fa5700f67ea4a12"
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
