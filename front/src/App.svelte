<script>
  import { Router } from "@roxi/routify";
  import { routes } from "../.routify/routes";
  AOS.init()
</script>

<style  global>
  @import "../assets/global.css";
</style>

<Router {routes} />