cask "kindle-comic-converter" do
  version "11.2.0"
  sha256 "7c12f1336bd8fba4f0a3b8af277258fbae5f3519ef00426b823a66c73547e7e3"

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
