let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixpkgs-unstable.tar.gz";
  pkgs = import nixpkgs {
    config = { };
    overlays = [ ];
  };
in

pkgs.mkShell {
  packages = with pkgs; [
    uv
    python313
    nodejs
  ];
}
