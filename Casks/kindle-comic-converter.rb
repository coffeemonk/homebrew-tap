cask "kindle-comic-converter" do
  version "11.3.2"
  sha256 "949d2042357762d9a2db6ecd6677ea6cd638a801bfd0662230b47b45ec2ac51e"

  url "https://github.com/ciromattia/kcc/releases/download/v#{version}/kcc_macos_arm_#{version}.dmg"
  name "Kindle Comic Converter"
  name "KCC"
  desc "Comic and manga converter for ebook readers"
  homepage "https://github.com/ciromattia/kcc"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on :macos

  app "Kindle Comic Converter.app"

  zap trash: "~/Library/Preferences/com.kindlecomicconverter.KindleComicConverter.plist"
end
