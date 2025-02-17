<script lang="ts">
    import { T } from "@threlte/core";
    import { Grid, OrbitControls, interactivity } from "@threlte/extras";
    import { spring } from "svelte/motion";

    interactivity();

    const scale = spring(1);

    let beacon_pos = $state([1, 1, 1]);
    let op_message = $state("Hello");

    // setInterval(() => {
    //     beacon_pos = [
    //         Math.random() * 10,
    //         Math.random() * 10,
    //         Math.random() * 10,
    //     ];
    // }, 1000);

    // setInterval(() => {
    //     beacon_pos = beacon_pos.map((value) => {
    //         // Calculate 20% of the current value
    //         const adjustment = value * 0.6;
    //         // Randomly decide to add or subtract the adjustment
    //         const newValue =
    //             Math.random() < 0.5 ? value + adjustment : value - adjustment;
    //         return newValue;
    //     });
    // }, 1000);

    const eventSource = new EventSource("http://localhost:8000/stream");
    eventSource.addEventListener("new_message", (event) => {
        const { position } = JSON.parse(event.data);
        console.log(position);
        beacon_pos = position;
    });
</script>

<T.PerspectiveCamera makeDefault position={[15, 15, 15]}>
    <OrbitControls />
</T.PerspectiveCamera>

<T.DirectionalLight position={[3, 10, 7]} intensity={Math.PI} />

<T.AmbientLight intensity={0.3} />

<T.Group scale={$scale}>
    <T.Mesh position.y={2.5} position.x={5} position.z={10}>
        <T.BoxGeometry args={[1, 5, 1]} />
        <T.MeshStandardMaterial color="#FE3D00" toneMapped={false} />
    </T.Mesh>
    <T.Mesh position={[beacon_pos[0], beacon_pos[1], beacon_pos[2]]}>
        <T.SphereGeometry args={[0.5]} />
        <T.MeshStandardMaterial color="#34ebe8" toneMapped={false} />
    </T.Mesh>
</T.Group>
<Grid cellColor="#FE3D00" sectionColor="#FE3D00" />
