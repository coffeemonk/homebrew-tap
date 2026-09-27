cask "kindle-comic-converter" do
  version "12.0.0"
  sha256 "bbfd451af6c215949b5b6e040152e577da2023b3684ace726c6b9e777ad7540b"

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
