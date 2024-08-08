{ pkgs }: {
  deps = [
    pkgs.python312Packages.flask
    pkgs.uwhoisd
    pkgs.bashInteractive
    pkgs.nodePackages.bash-language-server
    pkgs.man
  ];
}