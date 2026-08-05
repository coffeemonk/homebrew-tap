class WorkflowyCli < Formula
  desc "Command-line interface and MCP server for Workflowy"
  homepage "https://github.com/rodolfo-terriquez/workflowy-cli"
  version "3.3.2"

  on_macos do
    on_arm do
      url "https://github.com/rodolfo-terriquez/workflowy-cli/releases/download/v#{version}/wf-v#{version}-macos-arm64"
      sha256 "0712a851a6dde3f483ab9daad4764bb534150c5cabac2993ea56bcf5b1415b4f"
    end
    on_intel do
      url "https://github.com/rodolfo-terriquez/workflowy-cli/releases/download/v#{version}/wf-v#{version}-macos-x64"
      sha256 "f588ff4666dd3e9535bcb9daad4764bb534150c5cabac2993ea56bcf5b1415b4f"
    end
  end

  def install
    binary_name = Hardware::CPU.arm? ? "wf-v#{version}-macos-arm64" : "wf-v#{version}-macos-x64"
    bin.install binary_name => "wf"
  end

  test do
    output = shell_output("#{bin}/wf --version 2>&1", 0)
    assert_match "workflowy-cli", output.downcase
  end
end
