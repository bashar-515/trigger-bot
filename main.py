import asyncio
import os
from typing import Tuple, Optional

from dotenv import load_dotenv

from viam.robot.client import RobotClient
from viam.components.generic import Generic

load_dotenv()

async def connect() -> RobotClient:
    api_key = os.environ["API_KEY"]
    api_key_id = os.environ["API_KEY_ID"]
    address = os.environ["ADDRESS"]

    opts = RobotClient.Options.with_api_key(
        api_key=api_key,
        api_key_id=api_key_id
    )

    return await RobotClient.at_address(address, opts)

def validate(number: str) -> Tuple[bool, Optional[float]]:
    try:
        return True, float(number)
    except ValueError:
        return False, None

async def main() -> None:
    machine = await connect()
    generic_component = Generic.from_robot(machine, "generic-1")

    while True:
        is_valid, number = validate(input("enter a number to echo: "))

        if is_valid:
            if number == 0:
                break 

            response = await generic_component.do_command({
                "name": "number",
                "number": number
            })

            print(response)
        else:
            print("invalid")


    await machine.close()


if __name__ == "__main__":
    asyncio.run(main())
