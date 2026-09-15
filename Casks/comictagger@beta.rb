cask "comictagger@beta" do
  version "1.6.0-beta.10"
  sha256 "feb3ee3dc57483258dfb783aa4e63ce5928d3c094e6d184a8d0decb87f4c7019"

  url "https://github.com/comictagger/comictagger/releases/download/#{version}/ComicTagger-1.6.0b10-macOS-14.8.2-arm64.dmg"
  name "ComicTagger"
  desc "Metadata editor for digital comics"
  homepage "https://github.com/comictagger/comictagger"

  livecheck do
    url :url
    regex(/^v?(\d+(?:\.\d+)+(?:[._-]beta[._-]\d+)?)$/i)
  end

  conflicts_with cask: "comictagger"
  depends_on arch: :arm64
  depends_on :macos

  app "ComicTagger.app"

  zap trash: [
    "~/.ComicTagger",
    "~/Library/Application Support/ComicTagger",
    "~/Library/Preferences/ComicTagger.plist",
    "~/Library/Saved Application State/ComicTagger.savedState",
  ]
end
